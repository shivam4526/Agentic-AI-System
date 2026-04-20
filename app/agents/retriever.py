from __future__ import annotations

import asyncio
from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import StepDefinition, TaskRecord
from app.services.llm import detect_task_type


class RetrieverAgent(BaseAgent):
    agent_name = "retriever"

    async def run(self, task: TaskRecord, step: StepDefinition, dependency_outputs: dict[int, Any]) -> dict[str, Any]:
        await asyncio.sleep(0.1)
        task_type = step.payload.get("task_type") or detect_task_type(task.user_task)
        simulated_documents = self._documents_for_task(task.user_task, task_type, step.step_id)
        return {
            "documents": simulated_documents,
            "summary": f"Retrieved {len(simulated_documents)} documents for '{step.task}'",
            "dependencies": dependency_outputs,
        }

    def _documents_for_task(self, user_task: str, task_type: str, step_id: int) -> list[dict[str, str]]:
        base = [{"source": "internal_kb", "content": f"Context for task: {user_task}"}]

        tailored = {
            "leave_email": [
                {"source": "hr_policy_stub", "content": "Leave request emails should include subject, date range, reason, and a professional close."},
                {"source": "manager_expectation_stub", "content": "A concise tone with workload handoff reassurance improves approval likelihood."},
            ],
            "meeting_notes": [
                {"source": "meeting_stub", "content": "Effective meeting notes capture key discussion points, decisions made, and action items with owners."},
                {"source": "ops_stub", "content": "A short summary plus bulleted actions is easiest for teams to scan later."},
            ],
            "resume": [
                {"source": "career_stub", "content": "Strong resumes emphasize measurable impact, relevant skills, and concise experience bullets."},
                {"source": "recruiter_stub", "content": "Role alignment and keywords should be reflected in the professional summary and achievements."},
            ],
            "cover_letter": [
                {"source": "job_stub", "content": "A strong cover letter explains motivation, fit, and the most relevant experience for the target role."},
                {"source": "recruiter_stub", "content": "The best letters connect company goals with past outcomes in a personal but professional tone."},
            ],
            "support_reply": [
                {"source": "support_playbook_stub", "content": "Good support replies acknowledge the issue, explain the next step, and keep the tone empathetic."},
                {"source": "sla_stub", "content": "Response drafts should confirm ownership and set expectations clearly."},
            ],
            "proposal": [
                {"source": "proposal_stub", "content": "Effective proposals outline objectives, scope, approach, timeline, and expected outcomes."},
                {"source": "client_stub", "content": "Decision-makers respond well to clear deliverables and implementation confidence."},
            ],
            "action_plan": [
                {"source": "execution_stub", "content": "Action plans work best when they prioritize key steps, owners, risks, and near-term milestones."},
                {"source": "strategy_stub", "content": "Short horizon priorities and measurable next actions make plans easier to execute."},
            ],
        }.get(
            task_type,
            [{"source": "api_stub", "content": f"Retrieved facts for step {step_id}"}],
        )

        if task_type != "general":
            tailored.append({"source": "api_stub", "content": f"Retrieved facts for step {step_id}"})

        return base + tailored
