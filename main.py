from datetime import datetime
from uuid import UUID

from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from objects.commands import AddTask, Command
from objects.events import Event
from repositories.coordinator_repository import SQLiteCoordinatorRepository
from repositories.task_repository import TaskRepository, SQLiteTaskRepository

task_repo = SQLiteTaskRepository("tasks.db")
coordinator_repo = SQLiteCoordinatorRepository("tasks.db")


def task_adder(add_task_command: AddTask):
    task_repo.add_task(add_task_command.task)
    if add_task_command.reschedule_interval is not None:
        raise NotImplementedError


def command_handler(command: Command):
    if isinstance(command, AddTask):
        task_adder(command)
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
    task_repo.add_task(Task(description=description, due=due))
    redirect("/add")


@route("/complete/<uuid_str>", method="POST")
def proc_complete_task(uuid_str: str):
    mark_complete(task_repo, UUID(uuid_str))
    redirect("/add")


@route("/kick/<uuid_str>", method="POST")
def proc_kick_task(uuid_str: str):
    # Supports only the default for now
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    task.kick()
    task_repo.update_task(task)
    redirect("/add")


run(host="0.0.0.0", port=8000)
