from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.models.schemas import StepDefinition, TaskRecord


class BaseAgent(ABC):
    agent_name: str

    @abstractmethod
    async def run(self, task: TaskRecord, step: StepDefinition, dependency_outputs: dict[int, Any]) -> dict[str, Any]:
        raise NotImplementedError
