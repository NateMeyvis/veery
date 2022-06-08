from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from objects.task import Task


class Event:
    pass


@dataclass
class TaskCompletion(Event):
    task: Task
    completed_at: datetime
