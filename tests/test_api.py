import pytest
from httpx import ASGITransport, AsyncClient

from app.api.stream import get_queue as get_stream_queue
from app.api.task import get_queue as get_task_queue
from app.api.task import get_state_store
from app.main import app
from app.core.queue import RedisQueue
from app.db.state_store import RedisStateStore


@pytest.mark.asyncio
async def test_submit_and_fetch_task(fake_redis):
    def state_store_override() -> RedisStateStore:
        return RedisStateStore(fake_redis)

    def task_queue_override() -> RedisQueue:
        return RedisQueue(fake_redis)

    app.dependency_overrides[get_state_store] = state_store_override
    app.dependency_overrides[get_task_queue] = task_queue_override
    app.dependency_overrides[get_stream_queue] = task_queue_override

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        create_response = await client.post(
            "/api/v1/tasks",
            json={"task": "Research customer churn drivers"},
        )
        assert create_response.status_code == 202
        task_id = create_response.json()["task_id"]

        snapshot_response = await client.get(f"/api/v1/tasks/{task_id}")
        assert snapshot_response.status_code == 200
        payload = snapshot_response.json()
        assert payload["task"]["task_id"] == task_id
        assert len(payload["task"]["steps"]) == 3

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_dashboard_and_list_tasks(fake_redis):
    def state_store_override() -> RedisStateStore:
        return RedisStateStore(fake_redis)

    def task_queue_override() -> RedisQueue:
        return RedisQueue(fake_redis)

    app.dependency_overrides[get_state_store] = state_store_override
    app.dependency_overrides[get_task_queue] = task_queue_override
    app.dependency_overrides[get_stream_queue] = task_queue_override

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        dashboard_response = await client.get("/")
        assert dashboard_response.status_code == 200
        assert "Agentic AI Platform" in dashboard_response.text

        await client.post(
            "/api/v1/tasks",
            json={"task": "Analyze quarterly customer complaints"},
        )

        list_response = await client.get("/api/v1/tasks")
        assert list_response.status_code == 200
        payload = list_response.json()
        assert len(payload) == 1
        assert payload[0]["user_task"] == "Analyze quarterly customer complaints"

    app.dependency_overrides.clear()
