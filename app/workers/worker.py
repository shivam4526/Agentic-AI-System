from __future__ import annotations

import asyncio

from app.agents.analyzer import AnalyzerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.writer import WriterAgent
from app.core.logging import logger
from app.core.queue import RedisQueue
from app.core.retry import with_retry
from app.db.redis_client import get_redis_client
from app.db.state_store import RedisStateStore
from app.models.schemas import AgentType, StepResult, StepStatus, StreamEvent, TaskStatus
from app.orchestrator.scheduler import Scheduler
from app.orchestrator.state_manager import StateManager


class AgentWorker:
    def __init__(self) -> None:
        redis = get_redis_client()
        self.queue = RedisQueue(redis)
        self.state_store = RedisStateStore(redis)
        self.scheduler = Scheduler(self.queue, self.state_store)
        self.agents = {
            AgentType.retriever: RetrieverAgent(),
            AgentType.analyzer: AnalyzerAgent(),
            AgentType.writer: WriterAgent(),
        }

    async def run_forever(self) -> None:
        while True:
            message = await self.queue.dequeue(self.queue.settings.agent_queue)
            if message is None:
                continue
            await self.process_message(message)

    async def process_message(self, message) -> None:
        task = await self.state_store.get_task(message.task_id)
        if task is None:
            logger.error("task_not_found", task_id=message.task_id, step_id=message.step_id)
            return

        step = next(step for step in task.steps if step.step_id == message.step_id)
        dependencies = StateManager.dependency_outputs(task, step)

        running = StepResult(
            task_id=task.task_id,
            step_id=step.step_id,
            agent=step.agent,
            status=StepStatus.running,
            output={"message": f"Running step {step.step_id}"},
            attempt=message.attempt,
        )
        task = await self.state_store.save_step_result(running)
        task.status = TaskStatus.running
        await self.state_store.save_task(task)
        await self.queue.publish_event(
            task.task_id,
            StreamEvent(
                task_id=task.task_id,
                status="in_progress",
                step_id=step.step_id,
                step=step.task,
                partial_result=f"{step.agent.value} is processing step {step.step_id}",
            ),
        )

        agent = self.agents[step.agent]

        async def operation():
            return await agent.run(task, step, dependencies)

        try:
            output = await with_retry(operation)
        except Exception as exc:  # noqa: BLE001
            failed = StepResult(
                task_id=task.task_id,
                step_id=step.step_id,
                agent=step.agent,
                status=StepStatus.failed,
                output={},
                error=str(exc),
                attempt=message.attempt + 1,
            )
            task = await self.state_store.save_step_result(failed)
            task.status = TaskStatus.failed
            task.failure_reason = f"Step {step.step_id} failed: {exc}"
            await self.state_store.save_task(task)
            await self.queue.publish_event(
                task.task_id,
                StreamEvent(
                    task_id=task.task_id,
                    status="failed",
                    step_id=step.step_id,
                    step=step.task,
                    error=str(exc),
                ),
            )
            logger.exception("step_failed", task_id=task.task_id, step_id=step.step_id)
            return

        completed = StepResult(
            task_id=task.task_id,
            step_id=step.step_id,
            agent=step.agent,
            status=StepStatus.completed,
            output=output,
            attempt=message.attempt,
        )
        task = await self.state_store.save_step_result(completed)
        await self.queue.publish_event(
            task.task_id,
            StreamEvent(
                task_id=task.task_id,
                status="step_completed",
                step_id=step.step_id,
                step=step.task,
                partial_result=output,
            ),
        )

        if StateManager.all_steps_completed(task):
            final_result = task.results[max(task.results)].output.get("report") or str(task.results[max(task.results)].output)
            task = await self.state_store.set_final_result(task.task_id, final_result)
            await self.queue.publish_event(
                task.task_id,
                StreamEvent(
                    task_id=task.task_id,
                    status="completed",
                    partial_result=final_result,
                ),
            )
            return

        await self.scheduler.dispatch_ready_steps(task)


async def main() -> None:
    worker = AgentWorker()
    await worker.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
