from dataclasses import dataclass
from typing import Optional

from repositories.coordinator_repository import CoordinatorRepository
from repositories.task_repository import TaskRepository


@dataclass
class Environment:
    task_repository: Optional[TaskRepository] = None
    coordinator_repository: Optional[CoordinatorRepository] = None
