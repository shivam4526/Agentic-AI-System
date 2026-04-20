import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.core.config import get_settings

T = TypeVar("T")


async def with_retry(
    operation: Callable[[], Awaitable[T]],
    *,
    max_attempts: int | None = None,
    base_delay: float | None = None,
) -> T:
    settings = get_settings()
    attempts = max_attempts or settings.max_retries
    delay = base_delay or settings.retry_base_seconds
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            return await operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == attempts:
                break
            await asyncio.sleep(delay * (2 ** (attempt - 1)))

    assert last_error is not None
    raise last_error
