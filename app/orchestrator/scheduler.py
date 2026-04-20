from __future__ import annotations

from app.core.config import get_settings
from app.core.queue import RedisQueue
from app.db.state_store import RedisStateStore
from app.models.schemas import QueueMessage, StepResult, StepStatus, StreamEvent, TaskRecord, TaskStatus
from app.orchestrator.state_manager import StateManager


class Scheduler:
    def __init__(self, queue: RedisQueue, state_store: RedisStateStore):
        self.queue = queue
        self.state_store = state_store
        self.settings = get_settings()

    async def dispatch_ready_steps(self, task: TaskRecord) -> TaskRecord:
        ready_steps = StateManager.ready_steps(task)
        if not ready_steps:
            return task

        for step in ready_steps:
            queued_result = StepResult(
                task_id=task.task_id,
                step_id=step.step_id,
                agent=step.agent,
                status=StepStatus.queued,
                output={"message": f"Queued step {step.step_id}"},
            )
            task = await self.state_store.save_step_result(queued_result)
            await self.queue.enqueue(
                self.settings.agent_queue,
                QueueMessage(
                    task_id=task.task_id,
                    step_id=step.step_id,
                    agent=step.agent,
                    payload=step.payload,
                ),
            )
            await self.queue.publish_event(
                task.task_id,
                StreamEvent(
                    task_id=task.task_id,
                    status="queued",
                    step_id=step.step_id,
                    step=step.task,
                    partial_result=f"Step {step.step_id} queued for {step.agent.value}",
                ),
            )

        task.status = TaskStatus.queued
        await self.state_store.save_task(task)
        return task
