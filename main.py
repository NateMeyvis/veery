from datetime import datetime, timedelta
from uuid import UUID

from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from objects.coordinator import KickoffCoordinator
from objects.commands import AddTask, Command
from objects.events import Event, TaskCompletion
from repositories.coordinator_repository import SQLiteCoordinatorRepository
from repositories.task_repository import TaskRepository, SQLiteTaskRepository

task_repo = SQLiteTaskRepository("tasks.db")
coordinator_repo = SQLiteCoordinatorRepository("tasks.db")


def task_completer(task_completion: TaskCompletion):
    # TODO(nwm): Rename to reflect the fact that it doesn't complete the task
    coordinators = coordinator_repo.check_task_by_uuid(task_completion.task.uuid)
    results = []
    for coordinator in coordinators:
        results.extend(coordinator.proc_event(task_completion))
    for result in results:
        handler(result)


def task_adder(add_task_command: AddTask):
    task_repo.add_task(add_task_command.task)
    if add_task_command.reschedule_interval is not None:
        coordinator = KickoffCoordinator(
            task_uuid_to_track = add_task_command.task.uuid,
            interval = add_task_command.reschedule_interval,
        )
        coordinator_repo.add(coordinator)


def handler(command_or_event: Command|Event):
    if isinstance(command_or_event, AddTask):
        task_adder(command_or_event)
    elif isinstance(command_or_event, TaskCompletion):
        task_completer(command_or_event)
    else:
        raise NotImplementedError


@route("/")
def list_tasks():
    active = [
        task
        for task in task_repo.get_all_tasks()
        if task.status == CompletionStatus.OUTSTANDING
    ]
    return task_display(active)


@route("/add")
def add_task():
    return task_display(
        [
            task
            for task in task_repo.get_all_tasks()
            if task.status == CompletionStatus.OUTSTANDING
        ]
    )


@route("/add", method="POST")
def proc_add_task():
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
    handler(command)
    redirect("/add")


@route("/complete/<uuid_str>", method="POST")
def proc_complete_task(uuid_str: str):
    mark_complete(task_repo, UUID(uuid_str))
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    event = TaskCompletion(task, datetime.now())
    handler(event)
    redirect("/add")


@route("/kick/<uuid_str>", method="POST")
def proc_kick_task(uuid_str: str):
    # Supports only the default for now
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    task.kick()
    task_repo.update_task(task)
    redirect("/add")


run(host="0.0.0.0", port=8000)
