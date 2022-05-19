from datetime import datetime
from uuid import uuid4

import pytest

from objects.task import CompletionStatus, Task


@pytest.mark.parametrize("task", [Task("do ten push-ups"), Task("do a sit-up", datetime.now()), Task("")])
def test_basic_task_creation(task):
    assert task


def test_equality():
    uuid = uuid4()
    t1 = Task("", None, CompletionStatus.OUTSTANDING, uuid)
    t2 = Task("", None, CompletionStatus.OUTSTANDING, uuid)
    assert t1 == t2

def test_task_is_initialized_without_due_date_if_not_provided():
    task_without_due_datetime = Task("foo")
    assert task_without_due_datetime.due is None

@pytest.mark.parametrize('description,due,status', [
    ["foo", None, CompletionStatus.OUTSTANDING],
    ["bar", datetime(2022, 1, 2, 3, 4, 5), CompletionStatus.OUTSTANDING],
    ["bar", datetime(2022, 1, 2, 3, 8, 5), CompletionStatus.WONT_DO]
])
def test_tasks_with_identical_fields_get_different_uuids(description, due, status):
    t1 = Task(description, due, status)
    t2 = Task(description, due, status)
    t3 = Task(description, due, status)
    assert t1.uuid != t2.uuid
    assert t2.uuid != t3.uuid
    assert t1.uuid != t3.uuid
