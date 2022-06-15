from datetime import datetime, timedelta
import pytest

from objects.handlers import handler
from objects.events import TaskCompletion
from objects.coordinator import KickoffCoordinator
from objects.task import Task


@pytest.fixture
def env(test_env, tasks):
    # The test environment, with tasks and coordinators added
    for task in tasks:
        test_env.task_repository.add_task(task)
    for task in tasks[0:1]:
        coordinator = KickoffCoordinator(task_uuid_to_track=task.uuid)
        test_env.coordinator_repository.add(coordinator)
    return test_env


@pytest.fixture
def env_after_completion(env, tasks):
    completion_time = datetime.now() - timedelta(seconds=1)
    task_with_coordinator = tasks[0]
    event = TaskCompletion(task_with_coordinator, completion_time)
    handler(env, event)
    return env


def test_exactly_three_outstanding_tasks(env_after_completion, tasks):
    all_tasks = env_after_completion.task_repository.get_all_tasks()
    outstanding_tasks = [t for t in all_tasks if t.status.name == "OUTSTANDING"]
    assert len(outstanding_tasks) == len(tasks)


def test_replacement_with_same_description(env_after_completion, tasks):
    new_tasks = env_after_completion.task_repository.get_all_tasks()
    descriptions = set([task.description for task in new_tasks])
    original_descriptions = set([task.description for task in tasks])
    assert descriptions == original_descriptions


def test_old_uuids_are_there(env_after_completion, tasks):
    new_tasks = env_after_completion.task_repository.get_all_tasks()
    new_uuids = set([task.uuid for task in new_tasks])
    original_uuids = set([task.uuid for task in tasks])
    assert tasks[1].uuid in new_uuids
    assert tasks[2].uuid in new_uuids


def test_new_uuid_exists(env_after_completion, tasks):
    new_tasks = env_after_completion.task_repository.get_all_tasks()
    new_uuids = set([task.uuid for task in new_tasks])
    original_uuids = set([task.uuid for task in tasks])
    only_new = new_uuids - original_uuids
    assert len(only_new) == 1
