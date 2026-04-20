from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import StepDefinition, TaskRecord
from app.services.llm import LLMService


class WriterAgent(BaseAgent):
    agent_name = "writer"

    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()

    async def run(self, task: TaskRecord, step: StepDefinition, dependency_outputs: dict[int, Any]) -> dict[str, Any]:
        report = await self.llm_service.generate_final(
            user_task=task.user_task,
            dependency_outputs=dependency_outputs,
        )
        return {
            "report": report,
            "summary": f"Writer prepared the final response for task {task.task_id}",
        }
