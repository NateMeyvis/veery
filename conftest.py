from datetime import datetime
import tempfile

import pytest

from objects.task import Task
from repositories.coordinator_repository import SQLiteCoordinatorRepository
from repositories.task_repository import SQLiteTaskRepository


@pytest.fixture
def tasks():
    return [
        Task("Do a thing", due=datetime(2022, 1, 7, 2, 9)),
        Task("do another thing"),
        Task("do yet another thing", due=datetime(2022, 4, 2, 4, 2)),
    ]


@pytest.fixture
def in_memory_repo():
    in_memory_repo = SQLiteTaskRepository(":memory:")
    in_memory_repo.connection.execute(SQLiteTaskRepository.CREATE_SCHEMA)
    yield in_memory_repo

@pytest.fixture
def in_memory_coordinator_repo():
    with tempfile.NamedTemporaryFile() as f:
        in_memory_repo = SQLiteCoordinatorRepository(f.name)
        in_memory_repo.connection.execute(SQLiteCoordinatorRepository.CREATE_SCHEMA)
        yield in_memory_repo
