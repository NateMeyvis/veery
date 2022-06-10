from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4, UUID

from objects.commands import Command, AddTask
from objects.events import Event, TaskCompletion
from objects.task import Task


class TaskCoordinator(ABC):
    @abstractmethod
    def proc_event(self, event: Event):
        raise NotImplementedError


class KickoffCoordinator(TaskCoordinator):
    def __init__(
        self,
        task_uuid_to_track: UUID,
        interval: timedelta = timedelta(days=1),
        uuid_: Optional[UUID] = None,
    ):
        self.current_task_uuid = task_uuid_to_track
        self.interval = interval  # After a task is completed, schedule the next one <interval> from its completion
        self.uuid = uuid_ or uuid4()

    def proc_event(self, event: Event) -> List[Command]:
        if (
            isinstance(event, TaskCompletion)
            and event.task.uuid == self.current_task_uuid
        ):
            next_task = Task(
                description=event.task.description,
                due=event.completed_at + self.interval

            )
            self.current_task_uuid = next_task.uuid
            return [AddTask(next_task)]
        return []
