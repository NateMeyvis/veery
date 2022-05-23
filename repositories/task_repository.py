from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from uuid import UUID

from typing import List, Optional

from objects.task import CompletionStatus, Task


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
    def retrieve_task_by_uuid(self, uuid: UUID) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def remove_task(self, task_to_remove: Task):
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_to_update: Task):
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
        assert len(separated) >= 4
        status = CompletionStatus(int(separated[-1]))
        due = TextFileTaskRepository._task_due_from_string(separated[-2])
        uuid = UUID(separated[-3])
        description = TextFileTaskRepository.SEPARATOR.join(separated[:-3])
        return Task(description=description, due=due, uuid=uuid, status=status)

    @staticmethod
    def _task_due_to_string(due_datetime: Optional[datetime]) -> str:
        if due_datetime is None:
            return TextFileTaskRepository.EMPTY_DUE_DATETIME_INDICATOR
        else:
            return due_datetime.isoformat()

    @staticmethod
    def task_to_string(to_serialize: Task) -> str:
        return TextFileTaskRepository.SEPARATOR.join([to_serialize.description, to_serialize.uuid.hex, TextFileTaskRepository._task_due_to_string(to_serialize.due), str(to_serialize.status.value)])

    def get_all_tasks(self):
        tasks = []
        with open(self._path) as f:
            for task_line in f.readlines():
                tasks.append(TextFileTaskRepository.task_from_string(task_line.strip()))
        return tasks

    def retrieve_task_by_uuid(self, uuid: UUID) -> Optional[Task]:
        for task in self.get_all_tasks():
            if task.uuid == uuid:
                return task
        return None

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

    def update_task(self, task_to_update: Task):
        retrieved = self.retrieve_task_by_uuid(task_to_update.uuid)
        if retrieved is None:
            raise ValueError(f"Cannot update task {task_to_update}: no task with its UUID exists.")
        self.remove_task(retrieved)
        self.add_task(task_to_update)

class SQLiteTaskRepository(TaskRepository):

    CREATE_SCHEMA = """CREATE TABLE tasks (
        uuid text NOT NULL PRIMARY KEY,
        description text,
        due int,
        status int)"""

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    @staticmethod
    def _result_column_to_task(column) -> Task:
        return Task(
            uuid=UUID(column[0]),
            description=column[1],
            due=datetime.fromtimestamp(column[2]),
            status=CompletionStatus(column[3])
        )

    @staticmethod
    def _task_to_values_string(task):
        return f"""
            (
            '{task.uuid.hex}',
            '{task.description}',
            {int(task.due.timestamp())},
            {task.status.value}
            )
        """

    def get_all_tasks(self) -> List[Task]:
        cursor = self.connection.cursor().execute("SELECT * FROM tasks")
        results = cursor.fetchall()
        return [SQLiteTaskRepository._result_column_to_task(result) for result in results]

    def retrieve_task_by_uuid(self, uuid: UUID) -> Optional[Task]:
        cursor = self.connection.cursor().execute(f"SELECT * FROM tasks WHERE uuid = '{uuid.hex}'")
        results = cursor.fetchall()
        if len(results) == 0:
            return None
        if len(results) > 1:
            raise ValueError(f"Found more than 1 task with UUID {uuid}.")
        return SQLiteTaskRepository._result_column_to_task(results[0])

    def remove_task(self, task_to_remove: Task):
        self.connection.cursor().execute(f"""DELETE FROM tasks WHERE uuid = '{uuid.hex}'""")
        self.connection.commit()

    def update_task(self, task_to_update: Task):
        self.connection.cursor().execute(f"""UPDATE tasks SET 
        description = '{task_to_update.description}',
        due = {int(task_to_update.due.timestamp())},
        status = {task_to_update.status.value}
        WHERE uuid = '{task_to_update.uuid.hex}'""")

    def add_task(self, task: Task):
        self.connection.cursor().execute(f"""INSERT INTO tasks VALUES {SQLiteTaskRepository._task_to_values_string(task)}""")

    def set_task_list(self, tasks):
        raise NotImplementedError
