from redis.asyncio import Redis

from app.core.config import get_settings


class RedisClientFactory:
    _client: Redis | None = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            cls._client = Redis.from_url(
                get_settings().redis_url,
                decode_responses=True,
            )
        return cls._client


def get_redis_client() -> Redis:
    return RedisClientFactory.get_client()
