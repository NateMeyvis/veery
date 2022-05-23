from datetime import datetime
import sqlite3

import pytest

from objects.task import CompletionStatus, Task
from repositories.task_repository import SQLiteTaskRepository



@pytest.fixture
def repo():
    repo = SQLiteTaskRepository(':memory:')
    repo.connection.cursor().execute(SQLiteTaskRepository.CREATE_SCHEMA)
    repo.connection.commit()
    return repo


def test_repo_smoke(repo):
    assert repo


@pytest.fixture
def initial_tasks():
    return [Task("foo", datetime(2022, 1, 1)), Task("bar"), Task("baz", datetime(2022, 3, 4, 5, 6, 7))]

def test_attempted_retrieval_returns_none_on_failed_search(repo, initial_tasks):
    for task in initial_tasks:
        repo.add_task(task)
    new_task = Task("foo_description")
    assert repo.retrieve_task_by_uuid(new_task.uuid) is None

@pytest.mark.parametrize("new_status", [CompletionStatus.COMPLETED, CompletionStatus.WONT_DO])
@pytest.mark.parametrize("new_due", [None, datetime(2022, 1, 2, 4, 5, 6)])
@pytest.mark.parametrize("new_description", ["foo", "bar", "baz", "Qux!!!!!"])
def test_update(repo, tasks, new_due, new_description, new_status, initial_tasks):
    for task in initial_tasks:
        repo.add_task(task)
    task_to_modify = initial_tasks[0]
    task_to_modify.description = new_description
    task_to_modify.due = new_due
    repo.update_task(task_to_modify)
    retrieved = repo.retrieve_task_by_uuid(task_to_modify.uuid)
    assert retrieved.description == new_description
    assert retrieved.due == new_due

@pytest.mark.parametrize('new_task_ix', (0, 1, 2))
def test_sql_repo_roundtrips(sql_repo, tasks, new_task_ix):
    for task in tasks:
        sql_repo.add_task(task)
    to_retrieve = tasks[new_task_ix]
    retrieved = sql_repo.retrieve_task_by_uuid(to_retrieve.uuid)
    assert to_retrieve == retrieved


@pytest.mark.parametrize('new_status', (CompletionStatus.WONT_DO, CompletionStatus.COMPLETED))
def test_sql_repo_updates(sql_repo, tasks, new_status):
    for task in tasks:
        sql_repo.add_task(task)
    to_modify = tasks[1]
    to_modify.status = new_status
    sql_repo.update_task(to_modify)
    retrieved = sql_repo.retrieve_task_by_uuid(to_modify.uuid)
    assert to_modify == retrieved

