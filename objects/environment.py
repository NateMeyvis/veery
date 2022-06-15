from dataclasses import dataclass
from typing import Optional

from repositories.coordinator_repository import (
    CoordinatorRepository,
    SQLiteCoordinatorRepository,
)
from repositories.task_repository import TaskRepository, SQLiteTaskRepository


@dataclass
class Environment:
    task_repository: Optional[TaskRepository] = None
    coordinator_repository: Optional[CoordinatorRepository] = None


def environment_for(env) -> Environment:
    if env == "main":
        return Environment(
            task_repository=SQLiteTaskRepository("tasks.db"),
            coordinator_repository=SQLiteCoordinatorRepository("tasks.db"),
        )
    raise ValueError(f"{env} is not an environment")
