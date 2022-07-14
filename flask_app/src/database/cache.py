import abc
from datetime import timedelta
from typing import Optional, Any

from aioredis import Redis


class AsyncCacheStorage(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    async def set(self, key: str):
        pass

    @abc.abstractmethod
    async def get(self, key: str, data: Any):
        pass


class RedisStorage(AsyncCacheStorage):
    def __init__(self, storage: Redis):
        self.redis = storage

    async def set(self, key: str, value: Any, expires: timedelta) -> Optional[Any]:
        self.redis.set(key, "", ex=expires)

    async def get(self, key: str, data: any):
        self.redis.get(key)


