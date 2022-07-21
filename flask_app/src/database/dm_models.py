import datetime
import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID

from .db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.login}>'

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()


class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime,  default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<LoginHistory {self.user_id}:{self.auth_date}>'


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Roles {self.name}>'


class UsersRoles(db.Model):
    """связь пользователя и роли.
    Одному пользователю может быть назначено несколько ролей """
    __tablename__ = 'users_roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Roles.id))


class SocialAccount(db.Model):
    """Model to represent User social account."""

    __tablename__ = "social_accounts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,  unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

    social_id = db.Column(db.String, nullable=False)
    social_name = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("social_id", "social_name", name="social_pk"),
    )

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"

    @staticmethod
    def get(social_id: str, social_name: str):
        """Get or create social account instance."""

        social_account = SocialAccount.query.filter_by(
            social_id=social_id,
            social_name=social_name,
        ).first()
        if social_account is not None:
            return social_account
