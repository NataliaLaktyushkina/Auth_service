from datetime import datetime
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID

from .db import db


def create_partition_for_users(target, connection, **kw) -> None:
    """Create users partition by date of birth."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_1920_to_1979"
        PARTITION OF "users"
        FOR VALUES FROM ('1920-01-01') TO ('1979-12-31');
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_1980_to_2003"
        PARTITION OF "users"
        FOR VALUES FROM ('1980-01-01') TO ('2003-12-31');
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "users_birthdays_2004_to_2022"
        PARTITION OF "users"
        FOR VALUES FROM ('2004-01-01') TO ('2022-12-31');
        """
    )


class User(db.Model):
    """Model to represent user data """
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("id", "email", "date_of_birth"),
        {
            "postgresql_partition_by": "RANGE (date_of_birth)",
            "listeners": [("after_create", create_partition_for_users)],
        },
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    date_of_birth = db.Column(db.Date, primary_key=True,
                              default=datetime.today().date())

    def __repr__(self):
        return f'<User {self.login}>'

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()


class LoginHistory(db.Model):
    """Model to represent history of authorizations"""
    __tablename__ = 'login_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime,  default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return f'<LoginHistory {self.user_id}:{self.auth_date}>'


class Roles(db.Model):
    """Model to represent roles"""
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Roles {self.name}>'


class UsersRoles(db.Model):
    """Model to represent link btn users and roles
    One user -> many roles """
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
    def get(social_id: str, social_name: str, email:str):
        """Get or create social account instance."""

        social_account = SocialAccount.query.filter_by(
            social_id=social_id,
            social_name=social_name,
        ).first()
        if social_account is not None:
            return social_account
