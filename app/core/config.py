from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic AI System"
    app_env: Literal["local", "staging", "production"] = "local"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    redis_url: str = "redis://redis:6379/0"
    planner_queue: str = "planner_tasks"
    agent_queue: str = "agent_tasks"
    results_queue: str = "results"
    stream_channel_prefix: str = "stream"
    stream_history_prefix: str = "stream_history"
    stream_history_limit: int = Field(default=100, ge=1)
    task_key_prefix: str = "task"
    step_key_prefix: str = "step"

    max_retries: int = 3
    retry_base_seconds: float = 0.5
    worker_poll_timeout: int = 5
    worker_concurrency: int = 8
    llm_batch_size: int = Field(default=4, ge=1)
    llm_batch_window_ms: int = Field(default=75, ge=1)
    planner_mode: Literal["deterministic", "llm"] = "deterministic"
    llm_provider: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
