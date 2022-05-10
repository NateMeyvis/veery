import pytest

from objects.task import Task

def test_basic_task_creation():
    assert Task("do ten push-ups")

def test_task_can_be_created_with_empty_description():
    assert Task(description="")

def test_task_is_initialized_without_due_date_if_not_provided():
    task_without_due_datetime = Task("foo")
    assert task_without_due_datetime.due is None
