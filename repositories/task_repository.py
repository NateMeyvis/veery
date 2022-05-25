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


class SQLiteTaskRepository(TaskRepository):

    CREATE_SCHEMA = """CREATE TABLE tasks (
        uuid text NOT NULL PRIMARY KEY,
        description text,
        due datetime,
        status int)"""

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    @staticmethod
    def _values_tuple_to_task(column) -> Task:
        return Task(
            uuid=UUID(column[0]),
            description=column[1],
            due=datetime.fromisoformat(column[2]) if column[2] else None,
            status=CompletionStatus(column[3]),
        )

    @staticmethod
    def _task_to_values_tuple(task, rotated=False):  # Rotation for UPDATE order
        if not rotated:
            return (task.uuid.hex, task.description, task.due, task.status.value)
        else:
            return (task.description, task.due, task.status.value, task.uuid.hex)

    def get_all_tasks(self) -> List[Task]:
        cursor = self.connection.cursor().execute("SELECT * FROM tasks")
        results = cursor.fetchall()
        return [
            SQLiteTaskRepository._values_tuple_to_task(result) for result in results
        ]

    def retrieve_task_by_uuid(self, uuid: UUID) -> Optional[Task]:
        cursor = self.connection.cursor().execute(
            f"SELECT * FROM tasks WHERE uuid = '{uuid.hex}'"
        )
        results = cursor.fetchall()
        if len(results) == 0:
            return None
        if len(results) > 1:
            raise ValueError(f"Found more than 1 task with UUID {uuid}.")
        return SQLiteTaskRepository._values_tuple_to_task(results[0])

    def remove_task(self, task_to_remove: Task):
        self.connection.cursor().execute(
            f"""DELETE FROM tasks WHERE uuid = '{task_to_remove.uuid.hex}'"""
        )
        self.connection.commit()

    def update_task(self, task_to_update: Task):
        self.connection.cursor().execute(
            f"""UPDATE tasks SET 
        description = ?,
        due = ?,
        status = ?
        WHERE uuid = ?""",
            SQLiteTaskRepository._task_to_values_tuple(task_to_update, rotated=True),
        )

    def add_task(self, task: Task):
        self.connection.cursor().execute(
            f"""INSERT INTO tasks VALUES (?, ?, ?, ?)""",
            SQLiteTaskRepository._task_to_values_tuple(task),
        )
        self.connection.commit()
