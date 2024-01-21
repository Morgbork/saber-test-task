from typing import List

from pydantic import BaseModel


class TasksList(BaseModel):
    tasks: List[str]
