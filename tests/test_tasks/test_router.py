from unittest import mock

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
@mock.patch("src.tasks.service.get_sorted_tasks_from_build_name")
async def test_get_tasks(get_sorted_tasks_from_build_name_mocked) -> None:
    get_sorted_tasks_from_build_name_mocked.return_value = [
        "test_task_1",
        "test_task_2",
        "test_task_3",
    ]
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        r = await client.get("/get_tasks/?build=test_build")
        assert r.status_code == 200
        assert r.json() == {"tasks": ["test_task_1", "test_task_2", "test_task_3"]}
