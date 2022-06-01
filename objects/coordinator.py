from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from objects.commands import Command, AddTask
from objects.events import Event, TaskCompletion
from objects.task import Task


class TaskCoordinator(ABC):
    @abstractmethod
    def proc_event(self, event: Event):
        raise NotImplementedError


class KickoffCoordinator(TaskCoordinator):
    def __init__(
        self, tasks_to_track: List[Task], interval: timedelta = timedelta(days=1)
    ):
        self.task_uuids_to_track = set([t.uuid for t in tasks_to_track])
        self.interval = interval  # After a task is completed, schedule the next one <interval> from its completion

    def proc_event(self, event: Event) -> List[Command]:
        if (
            isinstance(event, TaskCompletion)
            and event.task.uuid in self.task_uuids_to_track
        ):
            next_task = Task(
                description=event.task.description,
                due=event.completed_at + self.interval,
            )
            return [AddTask(next_task)]
        return []
