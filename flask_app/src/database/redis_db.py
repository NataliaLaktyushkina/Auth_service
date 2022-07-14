import redis

from utils import settings

redis_settings = settings.get_settings()
host = redis_settings.REDIS_HOST
port = redis_settings.REDIS_PORT

redis_app = redis.Redis(host=host, port=port, db=0)
