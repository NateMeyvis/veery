from abc import ABC, abstractmethod
from datetime import datetime

from typing import List, Optional

from objects.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def set_task_list(self, tasks: List[Task]):
        raise NotImplementedError

    @abstractmethod
    def add_task(self, new_task: Task):
        raise NotImplementedError

    @abstractmethod
    def remove_task(self, task_to_remove: Task):
        raise NotImplementedError


class TextFileTaskRepository(TaskRepository):
    EMPTY_DUE_DATETIME_INDICATOR = "NONE"
    SEPARATOR = ','

    def __init__(self, path: str):
        self._path = path
    
    @staticmethod
    def _task_due_from_string(serialized: str) -> Optional[datetime]:
        if serialized == TextFileTaskRepository.EMPTY_DUE_DATETIME_INDICATOR:
            return None
        else:
            return datetime.fromisoformat(serialized)

    @staticmethod
    def task_from_string(serialized: str) -> Task:
        separated = serialized.split(TextFileTaskRepository.SEPARATOR)
        due = TextFileTaskRepository._task_due_from_string(separated[-1])
        description = TextFileTaskRepository.SEPARATOR.join(separated[:-1])
        return Task(description=description, due=due)

    @staticmethod
    def _task_due_to_string(due_datetime: Optional[datetime]) -> str:
        if due_datetime is None:
            return TextFileTaskRepository.EMPTY_DUE_DATETIME_INDICATOR
        else:
            return due_datetime.isoformat()

    @staticmethod
    def task_to_string(to_serialize: Task) -> str:
        return f"{to_serialize.description}{TextFileTaskRepository.SEPARATOR}{TextFileTaskRepository._task_due_to_string(to_serialize.due)}"

    def get_all_tasks(self):
        tasks = []
        with open(self._path) as f:
            for task_line in f.readlines():
                tasks.append(TextFileTaskRepository.task_from_string(task_line.strip()))
        return tasks

    def set_task_list(self, tasks: List[Task]):
        with open(self._path, "w") as f:
            f.write(
                "\n".join(
                    [TextFileTaskRepository.task_to_string(task) for task in tasks]
                )
            )

    def add_task(self, new_task: Task):
        task_list = self.get_all_tasks()
        task_list.append(new_task)
        self.set_task_list(task_list)

    def remove_task(self, task_to_remove: Task):
        task_list = self.get_all_tasks()
        task_list = [task for task in task_list if task != task_to_remove]
        self.set_task_list(task_list)
