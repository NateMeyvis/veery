from dataclasses import dataclass

from objects.coordinator import TaskCoordinator
from objects.task import Task


class Command:
    pass


@dataclass
class AddTask(Command):
    task: Task
    coordinator: Optional[TaskCoordinator]
