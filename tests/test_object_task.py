from datetime import datetime

import pytest

from objects.task import Task


@pytest.mark.parametrize("task", [Task("do ten push-ups"), Task("do a sit-up", datetime.now()), Task("")])
def test_basic_task_creation(task):
    assert task


def test_task_is_initialized_without_due_date_if_not_provided():
    task_without_due_datetime = Task("foo")
    assert task_without_due_datetime.due is None
