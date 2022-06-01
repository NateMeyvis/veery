from typing import List
from uuid import UUID

from objects.coordinator import TaskCoordinator


class CoordinatorRepository:
    def add(self, task_coordinator: TaskCoordinator):
        raise NotImplementedError

    def check_task_by_uuid(self, task_uuid: UUID) -> List[TaskCoordinator]:
        raise NotImplementedError
