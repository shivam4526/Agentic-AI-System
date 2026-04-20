import pytest

from app.models.schemas import AgentType, QueueMessage, StepDefinition, TaskRecord, TaskStatus
from app.orchestrator.scheduler import Scheduler
from app.workers.worker import AgentWorker


@pytest.mark.asyncio
async def test_end_to_end_worker_progression(fake_redis, state_store, queue):
    task = TaskRecord(
        user_task="Research and summarize",
        status=TaskStatus.queued,
        steps=[
            StepDefinition(step_id=1, agent=AgentType.retriever, task="Fetch data"),
            StepDefinition(step_id=2, agent=AgentType.analyzer, task="Analyze", depends_on=[1]),
            StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2]),
        ],
    )
    await state_store.save_task(task)

    scheduler = Scheduler(queue, state_store)
    await scheduler.dispatch_ready_steps(task)

    worker = AgentWorker()
    worker.queue = queue
    worker.state_store = state_store
    worker.scheduler = scheduler

    for _ in range(3):
        message = await queue.dequeue(queue.settings.agent_queue, timeout=1)
        assert message is not None
        await worker.process_message(message)

    stored = await state_store.get_task(task.task_id)
    assert stored is not None
    assert stored.status == TaskStatus.completed
    assert stored.final_result is not None
