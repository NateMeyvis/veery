from datetime import datetime, timedelta
import pytest

from objects.coordinator import KickoffCoordinator, TaskCompletion
from objects.task import CompletionStatus, Task
from repositories.task_repository import SQLiteTaskRepository


def test_in_memory_repo_smoke(in_memory_repo):
    assert in_memory_repo


@pytest.fixture
def completed_task():
    return Task(
        "Tighten screws",
        due=datetime(2022, 5, 29, 12),
        status=CompletionStatus.COMPLETED,
    )


@pytest.fixture
def completion(completed_task):
    return TaskCompletion(task=completed_task, completed_at=datetime(2022, 5, 29, 11))


@pytest.fixture
def repo_after_kickoff(in_memory_repo, completed_task, completion):
    in_memory_repo.add_task(completed_task)
    coordinator = KickoffCoordinator(
        task_uuid_to_track=completed_task.uuid, interval=timedelta(days=7)
    )
    coordinator.proc_event(completion)
    yield in_memory_repo


def test_coordinator_does_not_alter_completed_task(repo_after_kickoff, completed_task):
    retrieved = repo_after_kickoff.retrieve_task_by_uuid(completed_task.uuid)
    assert retrieved and retrieved == completed_task


def test_coordinator_emits_appropriate_event(completion, completed_task):
    coordinator = KickoffCoordinator(
        task_uuid_to_track=completed_task.uuid, interval=timedelta(days=7)
    )
    result = coordinator.proc_event(completion)
    expected = Task(
        completed_task.description,
        completion.completed_at + timedelta(days=7),
        status=CompletionStatus.OUTSTANDING,
    )
    assert len(result) == 1
    emitted_event = result[0]
    emitted_event_task = emitted_event.task
    assert (
        expected.description == emitted_event_task.description
        and expected.status == emitted_event_task.status
        and expected.due == emitted_event_task.due
    )
