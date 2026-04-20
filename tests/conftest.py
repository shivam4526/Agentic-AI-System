import pytest_asyncio
from fakeredis.aioredis import FakeRedis

from app.core.queue import RedisQueue
from app.db.state_store import RedisStateStore


@pytest_asyncio.fixture
async def fake_redis():
    redis = FakeRedis(decode_responses=True)
    yield redis
    await redis.flushall()
    await redis.aclose()


@pytest_asyncio.fixture
async def state_store(fake_redis):
    return RedisStateStore(fake_redis)


@pytest_asyncio.fixture
async def queue(fake_redis):
    return RedisQueue(fake_redis)
