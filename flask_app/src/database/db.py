from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from utils import settings

db_settings = settings.get_settings()

username = db_settings.USERNAME
password = db_settings.PASSWORD
host = db_settings.HOST
port = db_settings.PORT
host_port = ':'.join((host, port))
database_name = db_settings.DATABASE_NAME

db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI =  f'postgresql://{username}:{password}@{host_port}/{database_name}'


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)