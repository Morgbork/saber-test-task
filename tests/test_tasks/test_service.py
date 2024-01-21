from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.tasks import service as task_service


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_builds_file_read")
async def test_get_tasks_from_build():
    assert [
        "build_teal_leprechauns",
        "coloring_aqua_centaurs",
        "coloring_navy_golems",
    ] == await task_service.get_tasks_from_build("forward_interest")


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_builds_file_read")
async def test_get_tasks_from_build__wrong_build():
    with pytest.raises(HTTPException) as exc:
        await task_service.get_tasks_from_build("unexisting_build")
    assert exc.value.detail == "Build with the specified name does not exist."
    assert exc.value.status_code == 404


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_builds_file_read")
async def test_get_tasks_from_build__multiple_builds():
    with pytest.raises(HTTPException) as exc:
        await task_service.get_tasks_from_build("repeating_build")
    assert exc.value.detail == "More than one build with this name have been found."
    assert exc.value.status_code == 400


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_tasks_file_read")
async def test_construct_filtered_tasks_graph(tasks_graph):
    build_tasks = ["build_teal_leprechauns", "enable_teal_gnomes"]
    assert await task_service.construct_filtered_tasks_graph(["unexisting_task"]) == {}
    assert await task_service.construct_filtered_tasks_graph(build_tasks) == tasks_graph


def test_topological_graph_sorting(tasks_graph):
    result = (
        "build_white_fairies",
        "enable_teal_gnomes",
        "bring_aqua_leprechauns",
        "bring_aqua_humans",
        "coloring_fuchsia_fairies",
        "build_teal_leprechauns",
    )
    assert result == task_service.topological_graph_sorting(tasks_graph)


def test_topological_graph_sorting__with_cycles(tasks_cycle_graph):
    with pytest.raises(HTTPException) as exc:
        task_service.topological_graph_sorting(tasks_cycle_graph)
    assert exc.value.detail == "Tasks file contains cycles."
    assert exc.value.status_code == 400


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_tasks_file_read")
@patch("src.tasks.service.get_tasks_from_build")
async def test_get_sorted_tasks_from_build_name(mock_get_tasks_from_build):
    mock_get_tasks_from_build.return_value = [
        "coloring_aqua_centaurs",
        "coloring_navy_golems",
        "build_teal_leprechauns",
    ]
    assert [
        "build_teal_leprechauns",
        "coloring_aqua_centaurs",
        "coloring_navy_golems",
    ] == await task_service.get_sorted_tasks_from_build_name("forward_interest")
