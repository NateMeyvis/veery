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
