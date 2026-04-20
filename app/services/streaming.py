from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from app.core.queue import RedisQueue
from app.models.schemas import StreamEvent


async def sse_event_generator(task_id: str, queue: RedisQueue) -> AsyncIterator[str]:
    history = await queue.get_event_history(task_id)
    for event in history:
        yield f"data: {json.dumps(event.model_dump(mode='json'))}\n\n"
        if event.status in {"completed", "failed"}:
            return

    pubsub = await queue.subscribe(task_id)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
            if message and message.get("data"):
                raw = message["data"]
                event = StreamEvent.model_validate_json(raw)
                yield f"data: {json.dumps(event.model_dump(mode='json'))}\n\n"
                if event.status in {"completed", "failed"}:
                    break
            else:
                await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe()
        await pubsub.close()
