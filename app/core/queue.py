from __future__ import annotations

import json

from redis.asyncio import Redis

from app.core.config import get_settings
from app.models.schemas import QueueMessage, StreamEvent


class RedisQueue:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.settings = get_settings()

    async def enqueue(self, queue_name: str, message: QueueMessage) -> None:
        await self.redis.lpush(queue_name, message.model_dump_json())

    async def dequeue(self, queue_name: str, timeout: int | None = None) -> QueueMessage | None:
        timeout = timeout if timeout is not None else self.settings.worker_poll_timeout
        payload = await self.redis.brpop(queue_name, timeout=timeout)
        if not payload:
            return None
        _, raw = payload
        return QueueMessage.model_validate_json(raw)

    async def publish_event(self, task_id: str, event: StreamEvent) -> None:
        channel = f"{self.settings.stream_channel_prefix}:{task_id}"
        history_key = f"{self.settings.stream_history_prefix}:{task_id}"
        payload = event.model_dump_json()
        async with self.redis.pipeline(transaction=True) as pipe:
            await (
                pipe.lpush(history_key, payload)
                .ltrim(history_key, 0, self.settings.stream_history_limit - 1)
                .publish(channel, payload)
                .execute()
            )

    async def subscribe(self, task_id: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"{self.settings.stream_channel_prefix}:{task_id}")
        return pubsub

    async def get_event_history(self, task_id: str) -> list[StreamEvent]:
        history_key = f"{self.settings.stream_history_prefix}:{task_id}"
        events = await self.redis.lrange(history_key, 0, -1)
        return [StreamEvent.model_validate_json(event) for event in reversed(events)]
