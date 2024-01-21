from typing import Dict, List, Tuple

import aiofiles
import yaml
from fastapi import HTTPException, status
from graphlib import CycleError, TopologicalSorter

from src.tasks import config as tasks_config


async def get_tasks_from_build(build_name: str) -> List[str]:
    async with aiofiles.open(tasks_config.BUILDS_FILE_PATH, "r") as builds_file:
        content = await builds_file.read()
        builds = yaml.safe_load(content)

    builds = builds["builds"]
    filtered_builds = [b for b in builds if b["name"] == build_name]

    if not filtered_builds:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build with the specified name does not exist.",
        )
    elif len(filtered_builds) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="More than one build with this name have been found.",
        )

    tasks = filtered_builds[0]["tasks"]
    return tasks


async def construct_filtered_tasks_graph(filter_tasks: List[str]) -> Dict[str, set]:
    """
    Gets all tasks from the file. Filters them to include only listed in filter_tasks
    and its dependencies.
    """

    def _filter_tasks(
        tasks: Dict, filter_tasks_list: List[str], output_graph: Dict[str, set]
    ):
        dependent_tasks = []
        for task in tasks:
            if task["name"] in filter_tasks_list:
                output_graph.update({task["name"]: set(task["dependencies"])})
                dependent_tasks.extend(task["dependencies"])
        if dependent_tasks:
            _filter_tasks(tasks, dependent_tasks, output_graph)

    async with aiofiles.open(tasks_config.TASKS_FILE_PATH, "r") as tasks_file:
        content = await tasks_file.read()
        tasks_dependencies = yaml.safe_load(content)

    tasks_dependencies = tasks_dependencies["tasks"]
    tasks_graph = {}

    _filter_tasks(tasks_dependencies, filter_tasks, tasks_graph)

    return tasks_graph


def topological_graph_sorting(tasks_graph: Dict[str, set]) -> Tuple[str]:
    ts = TopologicalSorter(tasks_graph)
    try:
        sorted_tasks = tuple(ts.static_order())
    except CycleError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tasks file contains cycles.",
        )
    return sorted_tasks


async def get_sorted_tasks_from_build_name(build_name: str) -> List[str]:
    build_tasks = await get_tasks_from_build(build_name)
    tasks_graph = await construct_filtered_tasks_graph(build_tasks)
    sorted_tasks = topological_graph_sorting(tasks_graph)

    sorted_build_tasks = [task for task in sorted_tasks if task in build_tasks]
    if missed_tasks := set(build_tasks) - set(sorted_build_tasks):
        sorted_build_tasks.extend(missed_tasks)
    return sorted_build_tasks
