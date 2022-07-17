from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from database.dm_models import User
from database.db_service import add_record_to_login_history
from flask import request
from flask_jwt_extended import get_jti
from database.redis_db import redis_app as storage
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)
REFRESH_EXPIRES = timedelta(days=30)


class Auth:

    def get_jwt_tokens(self, user: User):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        user_agent = request.headers['user_agent']

        # запись в БД попытки входа
        add_record_to_login_history(user, user_agent)

        # запись в Redis refresh token
        key = ':'.join(('user_refresh', user_agent, get_jti(refresh_token)))
        storage.set(key, str(user.id), ex=REFRESH_EXPIRES)

        return {"access_token": access_token,
                "refresh_token": refresh_token}

auth=Auth()