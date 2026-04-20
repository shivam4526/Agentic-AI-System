from fastapi import APIRouter, Depends, HTTPException, status

from app.db.redis_client import get_redis_client
from app.db.state_store import RedisStateStore
from app.models.schemas import (
    TaskAcceptedResponse,
    TaskRecord,
    TaskSnapshotResponse,
    TaskStatus,
    UserTaskRequest,
)
from app.orchestrator.planner import PlannerAgent
from app.orchestrator.scheduler import Scheduler
from app.core.queue import RedisQueue

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_state_store() -> RedisStateStore:
    return RedisStateStore(get_redis_client())


def get_queue() -> RedisQueue:
    return RedisQueue(get_redis_client())


@router.post("", response_model=TaskAcceptedResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_task(
    request: UserTaskRequest,
    state_store: RedisStateStore = Depends(get_state_store),
    queue: RedisQueue = Depends(get_queue),
) -> TaskAcceptedResponse:
    task = TaskRecord(user_task=request.task, metadata=request.metadata, status=TaskStatus.planning)
    await state_store.save_task(task)

    planner = PlannerAgent()
    plan = await planner.create_plan(request.task)
    task = await state_store.set_steps(task.task_id, plan.steps)

    scheduler = Scheduler(queue, state_store)
    task.status = TaskStatus.queued
    await state_store.save_task(task)
    await scheduler.dispatch_ready_steps(task)

    return TaskAcceptedResponse(task_id=task.task_id, status=task.status)


@router.get("/{task_id}", response_model=TaskSnapshotResponse)
async def get_task(
    task_id: str,
    state_store: RedisStateStore = Depends(get_state_store),
) -> TaskSnapshotResponse:
    task = await state_store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskSnapshotResponse(task=task)


@router.get("", response_model=list[TaskRecord])
async def list_tasks(
    state_store: RedisStateStore = Depends(get_state_store),
) -> list[TaskRecord]:
    return await state_store.list_tasks()
