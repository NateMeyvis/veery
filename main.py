from datetime import datetime
from uuid import UUID

from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from repositories.task_repository import TaskRepository, SQLiteTaskRepository

repo = SQLiteTaskRepository("tasks.db")


@route("/")
def list_tasks(task_repository: TaskRepository = repo):
    active = [
        task
        for task in task_repository.get_all_tasks()
        if task.status == CompletionStatus.OUTSTANDING
    ]
    return task_display(active)


@route("/add")
def add_task(task_repository: TaskRepository = repo):
    return task_display(
        [
            task
            for task in task_repository.get_all_tasks()
            if task.status == CompletionStatus.OUTSTANDING
        ]
    )


@route("/add", method="POST")
def proc_add_task(task_repository: TaskRepository = repo):
    description = request.forms.get("description")
    due = (
        datetime.fromisoformat(request.forms.get("due"))
        if request.forms.get("due")
        else None
    )
    task_repository.add_task(Task(description=description, due=due))
    redirect("/add")


@route("/complete/<uuid_str>", method="POST")
def proc_complete_task(uuid_str: str, task_repository: TaskRepository = repo):
    mark_complete(task_repository, UUID(uuid_str))
    redirect("/add")


@route("/kick/<uuid_str>", method="POST")
def proc_kick_task(uuid_str: str, task_repository: TaskRepository = repo):
    # Supports only the default for now
    task = task_repository.retrieve_task_by_uuid(UUID(uuid_str))
    task.kick()
    task_repository.update_task(task)
    redirect("/add")


run(host="0.0.0.0", port=8000)
