from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from objects.task import CompletionStatus, Task


@pytest.mark.parametrize(
    "task", [Task("do ten push-ups"), Task("do a sit-up", datetime.now()), Task("")]
)
def test_basic_task_creation(task):
    assert task


@pytest.mark.parametrize(
    "due", [datetime(2022, 1, 7, 2, 9), datetime(1999, 1, 4, 2), None]
)
def test_tasks_stamped_with_creation_time(due):
    approx_creation_time = datetime.now()
    new_task = Task(":)", due=due)
    assert new_task.created
    assert abs((new_task.created - approx_creation_time).seconds) < 0.01


def test_equality():
    uuid = uuid4()
    creation_time = datetime.now()
    t1 = Task("", None, CompletionStatus.OUTSTANDING, creation_time, uuid)
    t2 = Task("", None, CompletionStatus.OUTSTANDING, creation_time, uuid)
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


@pytest.mark.parametrize(
    "due_datetime",
    [
        datetime.now() + timedelta(seconds=30),
        datetime.now() + timedelta(days=1, seconds=45),
        datetime.now() + timedelta(days=1729),
    ],
)
def test_kick_default_duration_future_due_date(due_datetime):
    task = Task("foo", due=due_datetime)
    task.kick()
    intended_duration = timedelta(days=1)
    approximate_actual_duration = task.due - due_datetime
    assert abs(approximate_actual_duration.seconds - intended_duration.seconds) < 1


@pytest.mark.parametrize(
    "due_datetime",
    [
        datetime.now() - timedelta(seconds=30),
        datetime.now() - timedelta(days=1, seconds=45),
        datetime.now() - timedelta(days=1729),
    ],
)
def test_kick_default_duration_past_due_date(due_datetime):
    task = Task("foo", due=due_datetime)
    now = datetime.now()
    task.kick()
    intended_duration = timedelta(days=1)
    approximate_actual_duration = task.due - now
    assert abs(approximate_actual_duration.seconds - intended_duration.seconds) < 1


@pytest.mark.parametrize(
    "created,due,expected",
    [
        (datetime.now() - timedelta(days=7), None, True),
        (datetime.now() - timedelta(days=9), None, True),
        (datetime.now() - timedelta(days=6), None, False),
        (datetime.now() - timedelta(days=7), datetime.now(), False),
        (datetime.now() - timedelta(days=9), datetime.now(), False),
        (datetime.now() + timedelta(days=9), None, False),
    ],
)
def test_staleness_calculation(created, due, expected):
    task = Task("!", created=created, due=due)
    assert task.stale == expected


@pytest.mark.parametrize(
    "created",
    [
        (
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=14),
        )
    ],
)
@pytest.mark.parametrize(
    "due,expected",
    [
        (
            datetime.now() + timedelta(seconds=15),
            False,
        ),
        (
            datetime.now() - timedelta(seconds=15),
            True,
        ),
        (
            datetime.now() + timedelta(seconds=60 * 60 * 24 + 15),
            False,
        ),
        (
            datetime.now() - timedelta(seconds=60 * 60 * 24 + 15),
            True,
        ),
    ],
)
def test_overdue_calculation(created, due, expected):
    task = Task("!", created=created, due=due)
    assert task.overdue == expected
