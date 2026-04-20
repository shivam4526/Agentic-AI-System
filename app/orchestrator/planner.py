from __future__ import annotations

from app.models.schemas import AgentType, PlannerOutput, StepDefinition
from app.services.llm import detect_task_type


class PlannerAgent:
    async def create_plan(self, user_task: str) -> PlannerOutput:
        task_type = detect_task_type(user_task)
        step_text = {
            "leave_email": (
                "Fetch leave-request context and relevant scheduling details",
                "Analyze the appropriate tone, structure, and leave duration details",
                "Generate the final leave request email",
            ),
            "meeting_notes": (
                "Fetch the meeting context, decisions, and action items",
                "Analyze the discussion into clear notes and ownership items",
                "Generate the final meeting summary",
            ),
            "resume": (
                "Fetch professional background context and role alignment signals",
                "Analyze strengths, impact, and positioning for the resume",
                "Generate the final resume draft",
            ),
            "cover_letter": (
                "Fetch job context and candidate positioning details",
                "Analyze fit, motivation, and key experience highlights",
                "Generate the final cover letter",
            ),
            "support_reply": (
                "Fetch the customer issue context and support details",
                "Analyze the issue, desired resolution, and communication tone",
                "Generate the final customer support reply",
            ),
            "proposal": (
                "Fetch the project or client context and objectives",
                "Analyze goals, scope, and recommended execution plan",
                "Generate the final proposal draft",
            ),
            "action_plan": (
                "Fetch the challenge context and relevant operating details",
                "Analyze priorities, risks, and execution steps",
                "Generate the final action plan",
            ),
        }.get(
            task_type,
            (
                "Fetch supporting context and relevant data",
                "Analyze the retrieved context and extract actionable insights",
                "Generate the final user-facing response",
            ),
        )

        steps = [
            StepDefinition(
                step_id=1,
                agent=AgentType.retriever,
                task=step_text[0],
                payload={"query": user_task, "task_type": task_type},
            ),
            StepDefinition(
                step_id=2,
                agent=AgentType.analyzer,
                task=step_text[1],
                depends_on=[1],
                payload={"task_type": task_type},
            ),
            StepDefinition(
                step_id=3,
                agent=AgentType.writer,
                task=step_text[2],
                depends_on=[2],
                payload={"task_type": task_type},
            ),
        ]
        return PlannerOutput(steps=steps)
