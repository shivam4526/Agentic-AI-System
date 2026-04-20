import pytest

from app.agents.analyzer import AnalyzerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.writer import WriterAgent
from app.models.schemas import AgentType, StepDefinition, TaskRecord


@pytest.mark.asyncio
async def test_retriever_returns_documents():
    agent = RetrieverAgent()
    task = TaskRecord(user_task="Fetch data")
    step = StepDefinition(step_id=1, agent=AgentType.retriever, task="Fetch")
    result = await agent.run(task, step, {})
    assert "documents" in result


@pytest.mark.asyncio
async def test_analyzer_returns_summary():
    agent = AnalyzerAgent()
    task = TaskRecord(user_task="Analyze data")
    step = StepDefinition(step_id=2, agent=AgentType.analyzer, task="Analyze", depends_on=[1])
    result = await agent.run(task, step, {1: {"documents": ["x"]}})
    assert "analysis" in result


@pytest.mark.asyncio
async def test_writer_returns_report():
    agent = WriterAgent()
    task = TaskRecord(user_task="Write report")
    step = StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2])
    result = await agent.run(task, step, {2: {"analysis": "done"}})
    assert "report" in result


@pytest.mark.asyncio
async def test_writer_generates_leave_email():
    agent = WriterAgent()
    task = TaskRecord(user_task="write a email for the leave for 3 days")
    step = StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2])
    result = await agent.run(task, step, {2: {"analysis": "tone should be professional"}})
    assert "Subject: Leave Request for 3 Days" in result["report"]


@pytest.mark.asyncio
async def test_writer_generates_meeting_notes():
    agent = WriterAgent()
    task = TaskRecord(user_task="Create meeting notes for the weekly sync")
    step = StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2])
    result = await agent.run(task, step, {1: {"documents": [{"content": "Budget approved"}]}})
    assert "Meeting Notes:" in result["report"]
    assert "Action Items" in result["report"]


@pytest.mark.asyncio
async def test_writer_generates_support_reply():
    agent = WriterAgent()
    task = TaskRecord(user_task="Write a customer support reply for a delayed order")
    step = StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2])
    result = await agent.run(task, step, {2: {"analysis": "be empathetic"}})
    assert "Subject: Update on Your Request" in result["report"]


@pytest.mark.asyncio
async def test_writer_generates_proposal():
    agent = WriterAgent()
    task = TaskRecord(user_task="Draft a business proposal for a new analytics dashboard")
    step = StepDefinition(step_id=3, agent=AgentType.writer, task="Write", depends_on=[2])
    result = await agent.run(task, step, {1: {"documents": [{"content": "Deliverables should be phased"}]}})
    assert "Proposal:" in result["report"]
