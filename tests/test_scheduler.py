import pytest

from app.models.schemas import AgentType, StepDefinition, TaskRecord
from app.orchestrator.scheduler import Scheduler


@pytest.mark.asyncio
async def test_scheduler_queues_ready_steps(state_store, queue):
    task = TaskRecord(
        user_task="Prepare report",
        steps=[
            StepDefinition(step_id=1, agent=AgentType.retriever, task="Fetch data"),
            StepDefinition(step_id=2, agent=AgentType.analyzer, task="Analyze", depends_on=[1]),
        ],
    )
    await state_store.save_task(task)
    scheduler = Scheduler(queue, state_store)

    updated = await scheduler.dispatch_ready_steps(task)
    queued = await queue.dequeue(queue.settings.agent_queue, timeout=1)

    assert updated.results[1].status.value == "queued"
    assert queued is not None
    assert queued.step_id == 1
