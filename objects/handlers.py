from typing import Union

from objects.coordinator import KickoffCoordinator
from objects.commands import AddTask, Command
from objects.events import Event, TaskCompletion
from objects.environment import environment_for, Environment
from repositories.task_repository import TaskRepository, SQLiteTaskRepository


def task_completion_handler(env: Environment, task_completion: TaskCompletion):
    coordinator_repo = env.coordinator_repository
    coordinators = coordinator_repo.check_task_by_uuid(task_completion.task.uuid)
    results = []
    for coordinator in coordinators:
        results.extend(coordinator.proc_event(task_completion))
        coordinator_repo.update(coordinator)  # Persist updated task to track
    for result in results:
        handler(env, result)


def task_adder(env: Environment, add_task_command: AddTask):
    task_repo = env.task_repository
    coordinator_repo = env.coordinator_repository
    task_repo.add_task(add_task_command.task)
    if add_task_command.reschedule_interval is not None:
        coordinator = KickoffCoordinator(
            task_uuid_to_track=add_task_command.task.uuid,
            interval=add_task_command.reschedule_interval,
        )
        coordinator_repo.add(coordinator)


def handler(env: Environment, command_or_event: Union[Command, Event]):
    if isinstance(command_or_event, AddTask):
        task_adder(env, command_or_event)
    elif isinstance(command_or_event, TaskCompletion):
        task_completion_handler(env, command_or_event)
    else:
        raise NotImplementedError
