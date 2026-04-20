from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    pending = "pending"
    planning = "planning"
    queued = "queued"
    running = "running"
    failed = "failed"
    completed = "completed"


class StepStatus(str, Enum):
    pending = "pending"
    queued = "queued"
    running = "running"
    failed = "failed"
    completed = "completed"


class AgentType(str, Enum):
    retriever = "retriever"
    analyzer = "analyzer"
    writer = "writer"


class UserTaskRequest(BaseModel):
    task: str = Field(..., min_length=3)
    metadata: dict[str, Any] = Field(default_factory=dict)


class StepDefinition(BaseModel):
    step_id: int
    agent: AgentType
    task: str
    depends_on: list[int] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)


class PlannerOutput(BaseModel):
    steps: list[StepDefinition]


class QueueMessage(BaseModel):
    task_id: str
    step_id: int
    agent: AgentType
    payload: dict[str, Any] = Field(default_factory=dict)
    attempt: int = 0


class StepResult(BaseModel):
    task_id: str
    step_id: int
    agent: AgentType
    status: StepStatus
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    attempt: int = 0
    updated_at: datetime = Field(default_factory=utc_now)


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    user_task: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.pending
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    steps: list[StepDefinition] = Field(default_factory=list)
    results: dict[int, StepResult] = Field(default_factory=dict)
    final_result: str | None = None
    failure_reason: str | None = None


class StreamEvent(BaseModel):
    task_id: str
    status: str
    step_id: int | None = None
    step: str | None = None
    partial_result: Any | None = None
    error: str | None = None
    timestamp: datetime = Field(default_factory=utc_now)


class TaskAcceptedResponse(BaseModel):
    task_id: str
    status: TaskStatus


class TaskSnapshotResponse(BaseModel):
    task: TaskRecord
