from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import StepDefinition, TaskRecord
from app.services.llm import LLMService


class AnalyzerAgent(BaseAgent):
    agent_name = "analyzer"

    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()

    async def run(self, task: TaskRecord, step: StepDefinition, dependency_outputs: dict[int, Any]) -> dict[str, Any]:
        analysis = await self.llm_service.analyze_task(
            user_task=task.user_task,
            dependency_outputs=dependency_outputs,
            objective=step.task,
        )
        return {
            "analysis": analysis,
            "summary": f"Analysis completed for step {step.step_id}",
        }
