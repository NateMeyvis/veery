from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from objects import Task
from repositories.task_repository import TaskRepository

class Event:
    pass

class TaskCompletion(Event):
    task: Task
    completed_at: datetime

class TaskCoordinator(ABC):

    @abstractmethod
    def proc_event(event: Event):
        raise NotImplementedError

class KickoffCoordinator(TaskCoordinator):
    def __init__(self, interval = timedelta(days=1), repo: TaskRepository):
        self.interval = interval # After a task is completed, schedule the next one <interval> from its completion

    def proc_event(event: Event):
        if isinstance(event, TaskCompletion):
            next_task = Task(description = event.task.description,
                            due = event.completed_at + self.interval)
            repo.add_task(next_task)
