from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from objects.task import Task


class Command:
    pass


@dataclass
class AddTask(Command):
    task: Task
    reschedule_interval: Optional[timedelta] = None
