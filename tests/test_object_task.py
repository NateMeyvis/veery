from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from objects.task import CompletionStatus, Task


@pytest.mark.parametrize(
    "task", [Task("do ten push-ups"), Task("do a sit-up", datetime.now()), Task("")]
)
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


@pytest.mark.parametrize(
    "description,due,status",
    [
        ["foo", None, CompletionStatus.OUTSTANDING],
        ["bar", datetime(2022, 1, 2, 3, 4, 5), CompletionStatus.OUTSTANDING],
        ["bar", datetime(2022, 1, 2, 3, 8, 5), CompletionStatus.WONT_DO],
    ],
)
def test_tasks_with_identical_fields_get_different_uuids(description, due, status):
    t1 = Task(description, due, status)
    t2 = Task(description, due, status)
    t3 = Task(description, due, status)
    assert t1.uuid != t2.uuid
    assert t2.uuid != t3.uuid
    assert t1.uuid != t3.uuid

def test_kick_default_duration_no_due_date():
    task = Task("foo")
    now = datetime.now()
    task.kick()
    intended_duration = timedelta(days=1)
    approximate_actual_duration = task.due - now
    assert abs(approximate_actual_duration.seconds - intended_duration.seconds) < 1


@pytest.mark.parametrize('due_datetime', [
    datetime.now() + timedelta(seconds=30),
    datetime.now() + timedelta(days=1, seconds=45),
    datetime.now() + timedelta(days=1729)
])
def test_kick_default_duration_future_due_date(due_datetime):
    task = Task("foo", due=due_datetime)
    task.kick()
    intended_duration = timedelta(days=1)
    approximate_actual_duration = task.due - due_datetime
    assert abs(approximate_actual_duration.seconds - intended_duration.seconds) < 1

@pytest.mark.parametrize('due_datetime', [
    datetime.now() - timedelta(seconds=30),
    datetime.now() - timedelta(days=1, seconds=45),
    datetime.now() - timedelta(days=1729)
])
def test_kick_default_duration_past_due_date(due_datetime):
    task = Task("foo", due=due_datetime)
    now = datetime.now()
    task.kick()
    intended_duration = timedelta(days=1)
    approximate_actual_duration = task.due - now
    assert abs(approximate_actual_duration.seconds - intended_duration.seconds) < 1
