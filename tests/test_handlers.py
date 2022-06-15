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


def test_task_completion_with_coordinator(env, tasks):
    # Tasks 0 and 1 are the tasks with coordinators
    completion_time = datetime.now() - timedelta(seconds=1)
    for task in tasks[0:1]:
        event = TaskCompletion(task, completion_time)
        handler(env, event)
