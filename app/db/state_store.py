from __future__ import annotations

from redis.asyncio import Redis

from app.core.config import get_settings
from app.models.schemas import StepDefinition, StepResult, TaskRecord, TaskStatus, utc_now


class RedisStateStore:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.settings = get_settings()

    def _task_key(self, task_id: str) -> str:
        return f"{self.settings.task_key_prefix}:{task_id}"

    async def save_task(self, task: TaskRecord) -> None:
        await self.redis.set(self._task_key(task.task_id), task.model_dump_json())

    async def get_task(self, task_id: str) -> TaskRecord | None:
        raw = await self.redis.get(self._task_key(task_id))
        return TaskRecord.model_validate_json(raw) if raw else None

    async def update_status(self, task_id: str, status: TaskStatus, *, failure_reason: str | None = None) -> TaskRecord:
        task = await self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")
        task.status = status
        task.failure_reason = failure_reason
        task.updated_at = utc_now()
        await self.save_task(task)
        return task

    async def set_steps(self, task_id: str, steps: list[StepDefinition]) -> TaskRecord:
        task = await self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")
        task.steps = steps
        task.updated_at = utc_now()
        await self.save_task(task)
        return task

    async def save_step_result(self, result: StepResult) -> TaskRecord:
        task = await self.get_task(result.task_id)
        if task is None:
            raise KeyError(f"Task {result.task_id} not found")
        task.results[result.step_id] = result
        task.updated_at = result.updated_at
        await self.save_task(task)
        return task

    async def set_final_result(self, task_id: str, final_result: str, *, status: TaskStatus = TaskStatus.completed) -> TaskRecord:
        task = await self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")
        task.final_result = final_result
        task.status = status
        task.updated_at = utc_now()
        await self.save_task(task)
        return task

    async def list_tasks(self) -> list[TaskRecord]:
        tasks: list[TaskRecord] = []
        async for key in self.redis.scan_iter(match=f"{self.settings.task_key_prefix}:*"):
            raw = await self.redis.get(key)
            if raw:
                tasks.append(TaskRecord.model_validate_json(raw))
        return sorted(tasks, key=lambda task: task.created_at)
