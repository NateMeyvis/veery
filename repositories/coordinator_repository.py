import sqlite3

from typing import List
from uuid import UUID

from objects.coordinator import KickoffCoordinator, TaskCoordinator


class CoordinatorRepository:
    def add(self, task_coordinator: TaskCoordinator):
        raise NotImplementedError

    def check_task_by_uuid(self, task_uuid: UUID) -> List[TaskCoordinator]:
        raise NotImplementedError

class SQLiteCoordinatorRepository(CoordinatorRepository):
    CREATE_SCHEMA = f"""CREATE TABLE kickoff_coordinators (uuid text NOT NULL PRIMARY KEY, current_task_uuid text, interval_minutes int)"""
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    @staticmethod
    def _values_tuple_to_kickoff_coordinator(column) -> KickoffCoordinator:
        return KickoffCoordinator(
            uuid_ = UUID(column[0]),
            current_task_uuid = UUID(column[1]),
            interval = timedelta(seconds = column[2] * 60)
        )

    @staticmethod
    def _kickoff_coordinator_to_values_tuple(kickoff_coordinator):
        return (
            kickoff_coordinator.uuid.hex,
            kickoff_coordinator.current_task_uuid.hex,
            (kickoff_coordinator.interval.seconds / 60)
        )
