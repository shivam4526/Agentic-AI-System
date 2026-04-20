from __future__ import annotations

import asyncio
import re
from collections.abc import Sequence
from typing import Any

from app.core.config import get_settings


def detect_task_type(user_task: str) -> str:
    lowered = user_task.lower()
    if "leave" in lowered and ("email" in lowered or "mail" in lowered):
        return "leave_email"
    if "meeting" in lowered and any(word in lowered for word in {"notes", "summary", "minutes"}):
        return "meeting_notes"
    if "resume" in lowered or "cv" in lowered:
        return "resume"
    if "cover letter" in lowered:
        return "cover_letter"
    if any(word in lowered for word in {"support", "customer reply", "customer response", "complaint response", "apology email"}):
        return "support_reply"
    if any(word in lowered for word in {"proposal", "project proposal", "business proposal"}):
        return "proposal"
    if any(word in lowered for word in {"action plan", "roadmap", "plan"}):
        return "action_plan"
    if any(word in lowered for word in {"summary", "brief", "report", "executive"}):
        return "brief"
    return "general"


class LLMService:
    """Local-first response generator with task-aware behaviors."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def complete(self, prompt: str) -> str:
        await asyncio.sleep(0.05)
        return self._smart_complete(prompt)

    async def batch_complete(self, prompts: Sequence[str]) -> list[str]:
        batch_size = self.settings.llm_batch_size
        results: list[str] = []
        for index in range(0, len(prompts), batch_size):
            window = prompts[index : index + batch_size]
            await asyncio.sleep(self.settings.llm_batch_window_ms / 1000)
            results.extend([self._smart_complete(prompt) for prompt in window])
        return results

    async def analyze_task(
        self,
        *,
        user_task: str,
        dependency_outputs: dict[int, Any],
        objective: str,
    ) -> str:
        await asyncio.sleep(0.05)
        task_type = detect_task_type(user_task)
        docs = self._extract_documents(dependency_outputs)
        doc_points = [doc.get("content", "") for doc in docs if doc.get("content")]

        insights = [
            f"Primary request: {self._sentence_case(user_task)}.",
            f"Execution objective: {objective}.",
            f"Retrieved context count: {len(docs)} supporting items.",
        ]

        insights.extend(self._analysis_guidance(task_type, user_task))

        if doc_points:
            insights.append("Most relevant retrieved context:")
            insights.extend(f"- {point}" for point in doc_points[:3])

        return "\n".join(insights)

    async def generate_final(
        self,
        *,
        user_task: str,
        dependency_outputs: dict[int, Any],
    ) -> str:
        await asyncio.sleep(0.05)
        return self._generate_final_response(user_task, dependency_outputs)

    def _generate_final_response(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        task_type = detect_task_type(user_task)

        if task_type == "leave_email":
            return self._generate_leave_email(user_task)
        if task_type == "meeting_notes":
            return self._generate_meeting_notes(user_task, dependency_outputs)
        if task_type == "resume":
            return self._generate_resume(user_task, dependency_outputs)
        if task_type == "cover_letter":
            return self._generate_cover_letter(user_task, dependency_outputs)
        if task_type == "support_reply":
            return self._generate_support_reply(user_task)
        if task_type == "proposal":
            return self._generate_proposal(user_task, dependency_outputs)
        if task_type == "action_plan":
            return self._generate_action_plan(user_task, dependency_outputs)
        if task_type == "brief":
            return self._generate_structured_brief(user_task, dependency_outputs)
        return self._generate_general_response(user_task, dependency_outputs)

    def _analysis_guidance(self, task_type: str, user_task: str) -> list[str]:
        if task_type == "leave_email":
            return [
                f"The response should be a professional leave request for {self._extract_day_count(user_task)} day(s).",
                "The tone should stay polite, concise, and manager-friendly.",
                "The final draft should include a subject line, the leave duration, a brief reason placeholder, and a courteous close.",
            ]
        if task_type == "meeting_notes":
            return [
                "The response should organize the meeting into summary, key decisions, and action items.",
                "The output should be easy to scan for teammates after the meeting.",
            ]
        if task_type == "resume":
            return [
                "The response should emphasize measurable impact, relevant skills, and professional positioning.",
                "The final resume should be concise and aligned to hiring expectations.",
            ]
        if task_type == "cover_letter":
            return [
                "The response should connect motivation, role fit, and experience into a professional narrative.",
                "The final cover letter should sound tailored rather than generic.",
            ]
        if task_type == "support_reply":
            return [
                "The reply should acknowledge the issue, provide reassurance, and explain next steps clearly.",
                "The tone should remain calm, empathetic, and service-oriented.",
            ]
        if task_type == "proposal":
            return [
                "The response should cover objectives, scope, approach, and expected outcomes.",
                "The final draft should be persuasive but still structured and concrete.",
            ]
        if task_type == "action_plan":
            return [
                "The response should prioritize actions, owners, milestones, and immediate next steps.",
                "The plan should be execution-oriented and simple to follow.",
            ]
        if task_type == "brief":
            return [
                "The final response should be structured, easy to scan, and appropriate for a business audience.",
                "The output should highlight the main findings before adding supporting detail.",
            ]
        return [
            "The final response should answer the request directly in plain language.",
            "The output should favor clarity and usability over technical verbosity.",
        ]

    def _smart_complete(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "create a final user-facing response for task" in lowered:
            task = self._extract_between(prompt, "task '", "' using the prior outputs")
            return self._generate_final_response(task or "the request", {})
        if "analyze the following for task" in lowered:
            task = self._extract_between(prompt, "task '", "':")
            objective = self._extract_after(prompt, "Objective:")
            return "\n".join(
                [
                    f"Primary request: {self._sentence_case(task or 'the task')}.",
                    f"Execution objective: {(objective or 'Analyze the available context').strip()}.",
                    "The response should synthesize the retrieved context into a clear, user-facing answer.",
                ]
            )
        return self._generate_general_response(prompt, {})

    def _extract_documents(self, dependency_outputs: dict[int, Any]) -> list[dict[str, Any]]:
        documents: list[dict[str, Any]] = []
        for output in dependency_outputs.values():
            if isinstance(output, dict) and isinstance(output.get("documents"), list):
                documents.extend(document for document in output["documents"] if isinstance(document, dict))
        return documents

    def _generate_leave_email(self, user_task: str) -> str:
        day_count = self._extract_day_count(user_task)
        return "\n".join(
            [
                f"Subject: Leave Request for {day_count} Days",
                "",
                "Dear [Manager Name],",
                "",
                f"I would like to request leave for {day_count} days from [start date] to [end date] due to personal reasons.",
                "I will make sure my current responsibilities are up to date before I go and will hand over any urgent work if needed.",
                "",
                "Please let me know if you need any additional information.",
                "",
                "Sincerely,",
                "[Your Name]",
            ]
        )

    def _generate_meeting_notes(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        bullets = self._document_bullets(dependency_outputs)
        return "\n".join(
            [
                f"Meeting Notes: {self._sentence_case(user_task)}",
                "",
                "Summary",
                "The meeting focused on the main discussion themes and next-step alignment.",
                "",
                "Key Decisions",
                "- Confirm the agreed priorities for the next phase.",
                "- Keep the follow-up concise and owner-driven.",
                "",
                "Action Items",
                "- Owner A: Finalize the immediate next steps.",
                "- Owner B: Share any supporting updates with the team.",
                *(f"- Context reference: {bullet}" for bullet in bullets[:2]),
            ]
        )

    def _generate_resume(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        bullets = self._document_bullets(dependency_outputs)
        return "\n".join(
            [
                "Professional Summary",
                "Results-oriented professional with experience delivering measurable outcomes, cross-functional collaboration, and structured problem solving.",
                "",
                "Core Skills",
                "- Stakeholder communication",
                "- Process improvement",
                "- Execution planning",
                "",
                "Experience Highlights",
                "- Led initiatives that improved delivery quality and operational clarity.",
                "- Coordinated work across teams to drive timely execution.",
                *(f"- Supporting context: {bullet}" for bullet in bullets[:2]),
            ]
        )

    def _generate_cover_letter(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        return "\n".join(
            [
                "Dear Hiring Manager,",
                "",
                f"I am excited to apply for the opportunity related to {self._sentence_case(user_task)}.",
                "My background includes delivering meaningful outcomes, collaborating across teams, and communicating clearly with stakeholders.",
                "I am particularly motivated by the opportunity to contribute with a thoughtful, execution-focused approach and strong ownership mindset.",
                "",
                "Thank you for your time and consideration.",
                "",
                "Sincerely,",
                "[Your Name]",
            ]
        )

    def _generate_support_reply(self, user_task: str) -> str:
        return "\n".join(
            [
                "Subject: Update on Your Request",
                "",
                "Hello [Customer Name],",
                "",
                f"Thank you for reaching out regarding {self._sentence_case(user_task)}.",
                "I understand how important this is, and I am sorry for the inconvenience.",
                "Our team is reviewing the issue and we will share the next update as soon as possible.",
                "",
                "Please let us know if there is any additional detail you would like us to include while we investigate.",
                "",
                "Best regards,",
                "Support Team",
            ]
        )

    def _generate_proposal(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        bullets = self._document_bullets(dependency_outputs)
        approach_lines = bullets[:3] if bullets else ["Use a phased approach with clear milestones and deliverables."]
        return "\n".join(
            [
                f"Proposal: {self._sentence_case(user_task)}",
                "",
                "Objective",
                "Deliver a clear and practical approach that addresses the core need and supports confident decision-making.",
                "",
                "Scope",
                "- Discovery and requirement alignment",
                "- Execution planning",
                "- Delivery and review",
                "",
                "Recommended Approach",
                *(f"- {bullet}" for bullet in approach_lines),
                "",
                "Expected Outcome",
                "A structured plan with transparent execution and measurable progress.",
            ]
        )

    def _generate_action_plan(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        bullets = self._document_bullets(dependency_outputs)
        return "\n".join(
            [
                f"Action Plan: {self._sentence_case(user_task)}",
                "",
                "Immediate Priorities",
                "- Clarify the primary objective and success criteria.",
                "- Align owners for the first wave of work.",
                "",
                "Next Steps",
                "- Start with the highest-impact action first.",
                "- Review progress at a short, fixed interval.",
                *(f"- Context input: {bullet}" for bullet in bullets[:2]),
                "",
                "Risk Watch",
                "- Track blockers early and resolve them before they slow execution.",
            ]
        )

    def _generate_structured_brief(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        bullets = self._document_bullets(dependency_outputs)
        if not bullets:
            bullets = [
                "Relevant context was gathered and normalized for downstream reasoning.",
                "The analysis stage identified the central themes and user-facing takeaways.",
                "The final response is organized for quick executive review.",
            ]
        return "\n".join(
            [
                f"Executive Brief: {self._sentence_case(user_task)}",
                "",
                "Key Points",
                *(f"- {bullet}" for bullet in bullets[:3]),
                "",
                "Recommendation",
                "Proceed with the synthesized findings above and present them in a concise, decision-ready format.",
            ]
        )

    def _generate_general_response(self, user_task: str, dependency_outputs: dict[int, Any]) -> str:
        documents = self._extract_documents(dependency_outputs)
        context_line = (
            f"I reviewed {len(documents)} supporting context item(s) before drafting this response."
            if documents
            else "I prepared a direct response based on the request."
        )
        return "\n".join(
            [
                f"Response for: {self._sentence_case(user_task)}",
                "",
                context_line,
                "Here is a concise answer tailored to the request and ready for the user.",
            ]
        )

    def _document_bullets(self, dependency_outputs: dict[int, Any]) -> list[str]:
        return [doc.get("content", "") for doc in self._extract_documents(dependency_outputs) if doc.get("content")]

    def _extract_day_count(self, text: str) -> int:
        digit_match = re.search(r"\b(\d+)\s*(day|days)\b", text.lower())
        if digit_match:
            return int(digit_match.group(1))
        word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}
        for word, value in word_map.items():
            if re.search(rf"\b{word}\s+(day|days)\b", text.lower()):
                return value
        return 3

    def _sentence_case(self, text: str) -> str:
        cleaned = " ".join(text.split()).strip()
        if not cleaned:
            return ""
        return cleaned[0].upper() + cleaned[1:]

    def _extract_between(self, text: str, start: str, end: str) -> str | None:
        try:
            left = text.index(start) + len(start)
            right = text.index(end, left)
        except ValueError:
            return None
        return text[left:right]

    def _extract_after(self, text: str, marker: str) -> str | None:
        try:
            start = text.index(marker) + len(marker)
        except ValueError:
            return None
        return text[start:].strip()
