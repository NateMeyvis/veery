from datetime import datetime
import tempfile

import pytest

from objects.task import Task
from repositories.task_repository import TextFileTaskRepository


@pytest.fixture
def repo():
    with tempfile.NamedTemporaryFile() as f:
        return TextFileTaskRepository(path=f.name)


def test_repo_smoke(repo):
    assert repo


def test_setting(repo, tasks):
    repo.set_task_list(tasks)
    retrieved = repo.get_all_tasks()
    assert set(tasks) == set(retrieved)


def test_removal(repo, tasks):
    # Create a repository with some tasks.
    repo.set_task_list(tasks)

    # Remove one of them.
    task_to_remove = Task("do another thing") # One of the task descriptions from conftest.py.
    repo.remove_task(task_to_remove)

    # Make sure it's gone
    assert not any([task == task_to_remove for task in repo.get_all_tasks()])


@pytest.mark.parametrize(
    "initial_tasks",
    [
        [],  # Test empty initial task list
        [Task("foo")],
        [Task("foo"), Task("bar"), Task("baz")],
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz")],
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz", datetime(2022, 3, 4, 5, 6, 7))],
    ],
)
def test_addition(repo, initial_tasks):
    # Create a repository with some tasks.
    repo.set_task_list(initial_tasks)

    # Add another
    task_to_add = Task("Add me!")
    repo.add_task(task_to_add)

    # Make sure it's there
    assert any([task == task_to_add for task in repo.get_all_tasks()])


@pytest.mark.parametrize('task_to_retrieve', 
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz", datetime(2022, 3, 4, 5, 6, 7))])
def test_retrieval_when_repository_has_other_tasks(repo, tasks, task_to_retrieve):
    # load some other tasks in
    repo.set_task_list(tasks)
    uuid_to_search = task_to_retrieve.uuid
    repo.add_task(task_to_retrieve)
    assert repo.retrieve_task_by_uuid(uuid_to_search) == task_to_retrieve

@pytest.mark.parametrize('task_to_retrieve', 
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz", datetime(2022, 3, 4, 5, 6, 7))])
def test_retrieval_when_repository_does_not_have_other_tasks(repo, task_to_retrieve):
    repo.set_task_list([])
    uuid_to_search = task_to_retrieve.uuid
    repo.add_task(task_to_retrieve)
    assert repo.retrieve_task_by_uuid(uuid_to_search) == task_to_retrieve

@pytest.mark.parametrize(
    "initial_tasks",
    [
        [],  # Test empty initial task list
        [Task("foo")],
        [Task("foo"), Task("bar"), Task("baz")],
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz")],
        [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz", datetime(2022, 3, 4, 5, 6, 7))],
    ],
)
def test_attempted_retrieval_returns_none_on_failed_search(repo, initial_tasks):
    repo.set_task_list(initial_tasks)
    new_task = Task("foo_description")
    assert repo.retrieve_task_by_uuid(new_task.uuid) is None
