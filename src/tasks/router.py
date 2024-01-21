from fastapi import APIRouter

from src.tasks import service as tasks_service
from src.tasks.schemas import TasksList

tasks_router = APIRouter()


@tasks_router.get("/get_tasks/", response_model=TasksList, status_code=200)
async def get_tasks(build: str):
    """Returns topologically sorted tasks related to the build."""
    tasks = await tasks_service.get_sorted_tasks_from_build_name(build)
    response = {"tasks": tasks}
    return response
