from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from utils.logger import logger


def init_limiter(app: Flask):
    limiter = Limiter(key_func=get_remote_address,
                      default_limits=["60 per hour"])
    limiter.logger = logger
    limiter.init_app(app)

# @limiter.limit("1/second", error_message='chill!')