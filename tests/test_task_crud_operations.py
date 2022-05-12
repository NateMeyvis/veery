from main import get_all_tasks, remove_task
from random import choice


def test_get_all_tasks_has_tasks():
    assert get_all_tasks()


def test_removing_nonexistent_task_leaves_task_list_without_that_task():
    nonexistent_task = "".join([choice("abcdefgh012345") for _ in range(12)])
    remove_task(nonexistent_task)
    assert nonexistent_task not in get_all_tasks()
