import tempfile

import pytest

from objects.task import CompletionStatus
from repositories.task_repository import TextFileTaskRepository
from repositories.helpers.helpers import mark_complete

@pytest.fixture
def repo(tasks):
    with tempfile.NamedTemporaryFile() as f:
        repo = TextFileTaskRepository(path=f.name)
        return repo

def test_smoke(repo):
    pass

@pytest.mark.parametrize('tasks_ix', (0, 1, 2))
# There are three tasks in the tasks fixture.
def test_marking_complete(repo, tasks, tasks_ix):
    # Populate the repo
    repo.set_task_list(tasks)
    # Choose a task to mark complete
    task_to_mark = tasks[tasks_ix]
    mark_complete(repo, task_to_mark.uuid)
    retrieved = repo.retrieve_task_by_uuid(task_to_mark.uuid)
    assert retrieved.status == CompletionStatus.COMPLETED
