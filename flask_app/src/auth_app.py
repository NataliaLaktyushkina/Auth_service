from datetime import timedelta

import click
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask import request, send_from_directory
from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from api.v1.api_v1_blueprint import app_v1_blueprint
from database.db import db
from database.db import init_db
from database.db_service import get_users_roles, create_user, assign_role_to_user
from database.dm_models import Roles
from database.redis_db import redis_app
from utils.limiter import init_limiter
from utils import logger
from utils import settings
from services import oauth as oauth_service

ACCESS_EXPIRES = timedelta(hours=1)
REFRESH_EXPIRES = timedelta(days=30)

SWAGGER_URL = '/apidocs/'
API_URL = '/static/swagger_config.yml'
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

oauth_client = OAuth()


@click.command(name='create-superuser')
@click.argument('name', envvar='SUPERUSER_NAME')
@click.argument('password', envvar='SUPERUSER_PASS')
@with_appcontext
def create_superuser(name, password):
    superuser = create_user(username=name, password=password)
    db_role = Roles.query.filter_by(name='admin').first()
    if superuser and db_role:
        assign_role_to_user(superuser, db_role)
        logger.logger.info(msg='Superuser was created')
    else:
        logger.logger.error(msg='Error while creating superuser')


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = settings.get_settings().SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_EXPIRES

    app.cli.add_command(create_superuser)

    app.register_blueprint(swagger_blueprint)
    app.register_blueprint(app_v1_blueprint, url_prefix='/v1')

    oauth_client.init_app(app)
    app.secret_key = 'my secret'
    oauth_service.google = oauth_service.register_google(oauth_client)

    jwt = JWTManager(app)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)


    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        """
        Callback function to check if a JWT exists in the redis blocklist
        """
        user_agent = request.headers['user_agent']
        jti = jwt_payload["jti"]
        key = ':'.join((jti, user_agent))
        token_in_redis = redis_app.get(key)
        return token_in_redis is not None

    @jwt.additional_claims_loader
    def add_role_to_token(identity):
        """
        callback function used to add additional claims when creating a JWT
        """
        roles = get_users_roles(identity)
        is_administrator = False
        is_manager = False
        for role in roles:
            if role.name == 'admin':
                is_administrator = True
            if role.name == 'manager':
                is_manager = True

        return {'is_administrator': is_administrator,
                'is_manager': is_manager}

    return app


def app_with_db():
    app = create_app()
    init_db(app)
    init_limiter(app)
    app.app_context().push()
    app.run(port=5001)
    # return app


if __name__ == '__main__':
    app_with_db()

