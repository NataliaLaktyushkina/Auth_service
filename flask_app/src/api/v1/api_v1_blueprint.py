from flask import Blueprint
from .personal_account import sign_up, login, logout, refresh, login_history, change_login, change_password, user_by_id
from .roles import create_role, delete_role, change_role, roles_list
from .users_roles import users_roles, assign_role, detach_role
from .oauth import oauth_login, oauth_authorize

app_v1_blueprint = Blueprint("v1", __name__)

app_v1_blueprint.add_url_rule('/change_login', methods=["POST"], view_func=change_login)
app_v1_blueprint.add_url_rule('/change_password', methods=["POST"], view_func=change_password)
app_v1_blueprint.add_url_rule('/login', methods=["POST"], view_func=login)
app_v1_blueprint.add_url_rule('/login_history', methods=["GET"], view_func=login_history)
app_v1_blueprint.add_url_rule('/logout', methods=["DELETE"], view_func=logout)
app_v1_blueprint.add_url_rule('/refresh', methods=["GET"], view_func=refresh)
app_v1_blueprint.add_url_rule('/sign_up', methods=["POST"], view_func=sign_up)
app_v1_blueprint.add_url_rule('/user_by_id', methods=["GET"], view_func=user_by_id)

app_v1_blueprint.add_url_rule('/create_role', methods=["POST"], view_func=create_role)
app_v1_blueprint.add_url_rule('/delete_role', methods=["DELETE"], view_func=delete_role)
app_v1_blueprint.add_url_rule('/change_role', methods=["PUT"], view_func=change_role)
app_v1_blueprint.add_url_rule('/roles_list', methods=["GET"], view_func=roles_list)

app_v1_blueprint.add_url_rule('/users_roles', methods=["GET"], view_func=users_roles)
app_v1_blueprint.add_url_rule('/assign_role', methods=["POST"], view_func=assign_role)
app_v1_blueprint.add_url_rule('/detach_role', methods=["DELETE"], view_func=detach_role)

app_v1_blueprint.add_url_rule('/oauth_login', methods=["GET"], view_func=oauth_login)
app_v1_blueprint.add_url_rule('/oauth_authorize', methods=["GET"], view_func=oauth_authorize)
