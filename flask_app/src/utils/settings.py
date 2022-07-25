import os

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()


class Settings(BaseSettings):

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.getenv('SECRET_KEY')

    # postgres
    USERNAME = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('POSTGRES_HOST')
    PORT = os.getenv('POSTGRES_PORT')
    DATABASE_NAME = os.getenv('POSTGRES_DB')

    REDIS_PORT: str = os.getenv('REDIS_PORT')
    JAEGER_PORT: str = os.getenv('JAEGER_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PromSettings(Settings):

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    JAEGER_HOST: str = os.getenv('JAEGER_HOST')
    TRACING: bool = True


class DevSettings(Settings):

    REDIS_HOST: str
    JAEGER_HOST: str
    TRACING: bool = False

    class Config:
        fields = {
            "REDIS_HOST": {
                'env': 'REDIS_HOST_DEBUG'
            },
            "JAEGER_HOST": {
                'env': 'JAEGER_HOST_DEBUG'
            }

        }


class OAuthSettings(BaseSettings):

    OAUTH_SECRET_KEY: str = os.getenv("OAUTH_SECRET_KEY")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_ACCESS_TOKEN_URL: str = os.getenv("GOOGLE_ACCESS_TOKEN_URL")
    GOOGLE_AUTHORIZE_URL: str = os.getenv("GOOGLE_AUTHORIZE_URL")
    GOOGLE_API_BASE_URL: str = os.getenv("GOOGLE_API_BASE_URL")
    OAUTH_REDIRECT_URL: str = os.getenv("OAUTH_REDIRECT_URL")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_settings():
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return get_prom_settings()
    else:
        return get_dev_settings()


def get_prom_settings():
    return PromSettings()


def get_dev_settings():
    return DevSettings()


def get_oauth_settings():
    return OAuthSettings()
