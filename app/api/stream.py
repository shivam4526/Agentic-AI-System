from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.queue import RedisQueue
from app.db.redis_client import get_redis_client
from app.services.streaming import sse_event_generator

router = APIRouter(prefix="/stream", tags=["stream"])


def get_queue() -> RedisQueue:
    return RedisQueue(get_redis_client())


@router.get("/{task_id}")
async def stream_task(task_id: str, queue: RedisQueue = Depends(get_queue)) -> StreamingResponse:
    return StreamingResponse(
        sse_event_generator(task_id, queue),
        media_type="text/event-stream",
    )
