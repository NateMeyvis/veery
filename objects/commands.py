from dataclasses import dataclass
from typing import Optional

from objects.task import Task


class Command:
    pass


@dataclass
class AddTask(Command):
    task: Task
    coordinator: Optional = None
