from datetime import timedelta
import sqlite3

from typing import List
from uuid import UUID

from objects.coordinator import KickoffCoordinator, TaskCoordinator


class CoordinatorRepository:
    def add(self, task_coordinator: TaskCoordinator):
        raise NotImplementedError

    def check_task_by_uuid(self, task_uuid: UUID) -> List[TaskCoordinator]:
        """Given a task UUID, gives a list of coordinators coordinating it."""
        raise NotImplementedError

    def update(self, task_coordinator: TaskCoordinator):
        raise NotImplementedError


class SQLiteCoordinatorRepository(CoordinatorRepository):
    CREATE_SCHEMA = f"""CREATE TABLE kickoff_coordinators (uuid text NOT NULL PRIMARY KEY, current_task_uuid text, interval_minutes int)"""

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    @staticmethod
    def _values_tuple_to_kickoff_coordinator(column) -> KickoffCoordinator:
        return KickoffCoordinator(
            uuid_=UUID(column[0]),
            task_uuid_to_track=UUID(column[1]),
            interval=timedelta(seconds=column[2] * 60),
        )

    @staticmethod
    def _kickoff_coordinator_to_values_tuple(kickoff_coordinator):
        return (
            kickoff_coordinator.uuid.hex,
            kickoff_coordinator.current_task_uuid.hex,
            (kickoff_coordinator.interval.seconds / 60),
        )

    def add(self, task_coordinator: TaskCoordinator):
        if not isinstance(task_coordinator, KickoffCoordinator):
            raise NotImplementedError
        self.connection.cursor().execute(
            f"INSERT INTO kickoff_coordinators VALUES (?, ?, ?)",
            SQLiteCoordinatorRepository._kickoff_coordinator_to_values_tuple(
                task_coordinator
            ),
        )
        self.connection.commit()

    def check_task_by_uuid(self, task_uuid: UUID) -> List[TaskCoordinator]:
        # Currently only KickoffCoordinators are implemented
        results = self.connection.cursor().execute(
            f"SELECT * FROM kickoff_coordinators WHERE current_task_uuid = '{task_uuid.hex}'"
        )
        return [
            SQLiteCoordinatorRepository._values_tuple_to_kickoff_coordinator(result)
            for result in results
        ]

    def update(self, task_coordinator: TaskCoordinator):
        if not isinstance(task_coordinator, KickoffCoordinator):
            raise NotImplementedError
        #TODO(nwm) Support updating other fields if necessary
        self.connection.cursor().execute(
            f"UPDATE kickoff_coordinators SET current_task_uuid = '{task_coordinator.current_task_uuid.hex}' WHERE uuid = '{task_coordinator.uuid.hex}'")
        self.connection.commit()

