from http import HTTPStatus

from flask import jsonify, request, make_response, Response

from database.db_service import get_roles_by_user, assign_role_to_user, detach_role_from_user
from database.dm_models import Roles, User
from decorators import admin_required
from typing import Union


@admin_required()
def users_roles():
    username = request.json.get("username", None)
    if not username:
        return make_response('Username is empty', HTTPStatus.UNAUTHORIZED)
    users_roles = get_roles_by_user(username)
    output = [role.name for role in users_roles]
    return jsonify(roles=output)


@admin_required()
def assign_role():
    username = request.json.get("username", None)
    role = request.json.get("role", None)
    user_data = check_user_role(username, role)
    assign_role_to_user(user_data["user_db"], user_data["db_role"])
    return jsonify(msg=f'Role {role} was assigned to user {username}')


@admin_required()
def detach_role():
    username = request.json.get('username', None)
    role = request.json.get('role', None)
    user_data = check_user_role(username, role)
    detach_role_from_user(user_data["user_db"], user_data["db_role"])
    return jsonify(msg=f'Role {role} was  detached from user {username}')


def check_user_role(username: str, role: str) -> Union[dict, Response]:
    if not role or not username:
        return make_response('Role or username is empty', HTTPStatus.UNAUTHORIZED)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = User.query.filter_by(login=username).first()
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    user_data = {'db_role': db_role,
                 "user_db": user_db}
    return user_data
