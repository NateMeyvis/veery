from datetime import datetime, timedelta
from typing import Union
from uuid import UUID

from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from objects.coordinator import KickoffCoordinator
from objects.commands import AddTask, Command
from objects.environment import Environment
from objects.events import Event, TaskCompletion
from repositories.coordinator_repository import SQLiteCoordinatorRepository
from repositories.task_repository import TaskRepository, SQLiteTaskRepository


def environment_for(env) -> Environment:
    if env == "main":
        return Environment(
            task_repository=SQLiteTaskRepository("tasks.db"),
            coordinator_repository=SQLiteCoordinatorRepository("tasks.db"),
        )
    raise ValueError(f"{env} is not an environment")


def task_completion_handler(env, task_completion: TaskCompletion):
    coordinator_repo = environment_for(env).coordinator_repository
    coordinators = coordinator_repo.check_task_by_uuid(task_completion.task.uuid)
    results = []
    for coordinator in coordinators:
        results.extend(coordinator.proc_event(task_completion))
        coordinator_repo.update(coordinator)  # Persist updated task to track
    for result in results:
        handler(env, result)


def task_adder(env, add_task_command: AddTask):
    task_repo = environment_for(env).task_repository
    task_repo.add_task(add_task_command.task)
    if add_task_command.reschedule_interval is not None:
        coordinator = KickoffCoordinator(
            task_uuid_to_track=add_task_command.task.uuid,
            interval=add_task_command.reschedule_interval,
        )
        coordinator_repo.add(env, coordinator)


def handler(env, command_or_event: Union[Command, Event]):
    if isinstance(command_or_event, AddTask):
        task_adder(env, command_or_event)
    elif isinstance(command_or_event, TaskCompletion):
        task_completion_handler(env, command_or_event)
    else:
        raise NotImplementedError


@route("/<env>/")
def list_tasks(env: str):
    task_repo = environment_for(env).task_repository
    active = [
        task
        for task in task_repo.get_all_tasks()
        if task.status == CompletionStatus.OUTSTANDING
    ]
    return task_display(env, active)


@route("/<env>/add")
def add_task(env: str):
    task_repo = environment_for(env).task_repository
    return task_display(
        env,
        [
            task
            for task in task_repo.get_all_tasks()
            if task.status == CompletionStatus.OUTSTANDING
        ],
    )


@route("/<env>/add", method="POST")
def proc_add_task(env: str):
    task_repo = environment_for(env).task_repository
    description = request.forms.get("description")
    due = (
        datetime.fromisoformat(request.forms.get("due"))
        if request.forms.get("due")
        else None
    )
    raw_reschedule_interval = request.forms.get("reschedule_interval")
    reschedule_interval = (
        timedelta(days=int(raw_reschedule_interval))
        if raw_reschedule_interval
        else None
    )
    command = AddTask(
        task=Task(description=description, due=due),
        reschedule_interval=reschedule_interval,
    )
    handler(env, command)
    redirect(f"/{env}/add")


@route("/<env>/complete/<uuid_str>", method="POST")
def proc_complete_task(env: str, uuid_str: str):
    task_repo = environment_for(env).task_repository
    mark_complete(task_repo, UUID(uuid_str))
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    event = TaskCompletion(task, datetime.now())
    handler(env, event)
    redirect(f"/{env}/add")


@route("/<env>/kick/<uuid_str>", method="POST")
def proc_kick_task(env: str, uuid_str: str):
    task_repo = environment_for(env).task_repository
    # Supports only the default for now
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    task.kick()
    task_repo.update_task(task)
    redirect(f"/{env}/add")


run(host="0.0.0.0", port=8000)
