from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta

from objects.task import Task
from repositories.task_repository import TaskRepository


class Event:
    pass


@dataclass
class TaskCompletion(Event):
    task: Task
    completed_at: datetime


class TaskCoordinator(ABC):
    @abstractmethod
    def proc_event(self, event: Event):
        raise NotImplementedError


class KickoffCoordinator(TaskCoordinator):
    def __init__(self, repo: TaskRepository, interval: timedelta = timedelta(days=1)):
        self.interval = interval  # After a task is completed, schedule the next one <interval> from its completion
        self.repo = repo

    def proc_event(self, event: Event):
        if isinstance(event, TaskCompletion):
            next_task = Task(
                description=event.task.description,
                due=event.completed_at + self.interval,
            )
            self.repo.add_task(next_task)
