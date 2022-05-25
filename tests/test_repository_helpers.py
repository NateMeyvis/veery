import tempfile

import pytest

from objects.task import CompletionStatus
from repositories.task_repository import SQLiteTaskRepository
from repositories.helpers.helpers import mark_complete


@pytest.fixture
def repo():
    repo = SQLiteTaskRepository(":memory:")
    repo.connection.cursor().execute(SQLiteTaskRepository.CREATE_SCHEMA)
    repo.connection.commit()
    return repo


@pytest.mark.parametrize("tasks_ix", (0, 1, 2))
# There are three tasks in the tasks fixture.
def test_marking_complete(repo, tasks, tasks_ix):
    # Populate the repo
    for task in tasks:
        repo.add_task(task)
    # Choose a task to mark complete
    task_to_mark = tasks[tasks_ix]
    mark_complete(repo, task_to_mark.uuid)
    retrieved = repo.retrieve_task_by_uuid(task_to_mark.uuid)
    assert retrieved.status == CompletionStatus.COMPLETED
