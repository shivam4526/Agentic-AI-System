from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dashboard import router as dashboard_router
from app.api.stream import router as stream_router
from app.api.task import router as task_router
from app.core.config import get_settings
from app.core.logging import configure_logging, logger
from app.db.redis_client import get_redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    redis = get_redis_client()
    await redis.ping()
    logger.info("app_started")
    yield
    await redis.aclose()
    logger.info("app_stopped")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(dashboard_router)
    app.include_router(task_router, prefix="/api/v1")
    app.include_router(stream_router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
