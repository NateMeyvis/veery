import pytest

from objects.coordinator import KickoffCoordinator
from repositories.coordinator_repository import SQLiteCoordinatorRepository

@pytest.fixture
def repo():
    repo = SQLiteCoordinatorRepository(":memory:")
    repo.connection.execute(SQLiteCoordinatorRepository.CREATE_SCHEMA)
    yield repo

def test_repo_smoke(repo):
    assert repo

def test_repo_addition(repo, tasks):
    for task in tasks:
        repo.add(KickoffCoordinator(task_uuid_to_track=task.uuid))
    returned = repo.connection.execute("SELECT * FROM kickoff_coordinators").fetchall()
    coordinators = [SQLiteCoordinatorRepository._values_tuple_to_kickoff_coordinator(column) for column in returned]
    assert len(coordinators) == 3
    assert set([t.uuid for t in tasks]) == set([c.current_task_uuid for c in coordinators])

def test_repo_checking(repo, tasks):
    coordinators = [KickoffCoordinator(task_uuid_to_track=task.uuid) for task in tasks]
    for coordinator in coordinators:
        repo.add(coordinator)
    result = repo.check_task_by_uuid(tasks[1].uuid)
    assert len(result) == 1
    assert type(result[0]) == KickoffCoordinator
