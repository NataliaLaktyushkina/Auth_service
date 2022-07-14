import uuid
from datetime import datetime
from typing import List

from database.db import db
from werkzeug.security import generate_password_hash

from .dm_models import User, LoginHistory, Roles, UsersRoles


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()
    return user


def add_record_to_login_history(user: User, user_agent: str):
    # запись в БД попытки входа
    new_session = LoginHistory(user_id=user.id,
                               user_agent=user_agent,
                               auth_date=datetime.now())
    db.session.add(new_session)
    db.session.commit()


def create_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(login=username,
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def change_login_in_db(user: User, new_login: str):
    user.login = new_login
    db.session.commit()


def change_password_in_db(user: User, new_password: str):
    hashed_password = generate_password_hash(new_password, method='sha256')
    user.password = hashed_password
    db.session.commit()


def create_role_db(role_name: str) -> Roles:
    new_role = Roles(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return new_role


def get_users_roles(user_id : uuid) -> List[Roles]:
    users_roles = UsersRoles.query.filter_by(user_id=user_id).all()
    if not users_roles:
        return []
    output = []
    for role in users_roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        output.append(role)
    return output


def delete_role_db(role: Roles):
    db.session.delete(role)
    db.session.commit()


def change_role_db(role_name: str, new_name: str):
    role = Roles.query.filter_by(name=role_name).first()
    role.name = new_name
    db.session.commit()


def get_roles_by_user(username: str) -> List[Roles]:
    user = User.query.filter_by(login=username).first()
    roles = UsersRoles.query.filter_by(user_id=user.id).all()
    output = []
    for role in roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        output.append(role)
    return output


def assign_role_to_user(user: User, role: Roles):
    new_assignment = UsersRoles(user_id=user.id,
                                role_id=role.id)
    db.session.add(new_assignment)
    db.session.commit()


def detach_role_from_user(user: User, role: Roles):
    db.session.query(UsersRoles).filter_by(user_id=user.id,
                                           role_id=role.id).delete()
    db.session.commit()

