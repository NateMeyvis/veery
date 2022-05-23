import pytest
import sqlite3
from tempfile import NamedTemporaryFile

from repositories.task_repository import SQLiteTaskRepository

@pytest.fixture
def sql_repo():
    repo = SQLiteTaskRepository(':memory:')
    repo.connection.cursor().execute(SQLiteTaskRepository.CREATE_SCHEMA)
    repo.connection.commit()
    return repo

def test_sql_repo_smoke(sql_repo):
    assert sql_repo

def test_sql_repo_roundtrips(sql_repo, tasks):
    for task in tasks:
        sql_repo.add_task(task)
    
