import pytest

from app.orchestrator.planner import PlannerAgent


@pytest.mark.asyncio
async def test_planner_creates_three_stage_plan():
    planner = PlannerAgent()
    plan = await planner.create_plan("Research the market and write a summary")

    assert len(plan.steps) == 3
    assert plan.steps[0].agent.value == "retriever"
    assert plan.steps[1].depends_on == [1]
    assert plan.steps[2].depends_on == [2]
