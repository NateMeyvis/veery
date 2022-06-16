from datetime import datetime, timedelta
from typing import Union
from uuid import UUID

from bottle import jinja2_view, redirect, request, route, run, static_file

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from objects.coordinator import KickoffCoordinator
from objects.commands import AddTask, Command
from objects.environment import environment_for, Environment
from objects.events import Event, TaskCompletion
from objects.handlers import handler, task_completion_handler, task_adder
from repositories.coordinator_repository import SQLiteCoordinatorRepository
from repositories.task_repository import TaskRepository, SQLiteTaskRepository

@route("/base_css/")
def base_css():
    return static_file("base.css", root="static/")

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


@route("/<env>/add_jinja")
@jinja2_view("templates/task_list.html")
def add_task(env: str):
    task_repo = environment_for(env).task_repository
    tasks = [
        task
        for task in task_repo.get_all_tasks()
        if task.status == CompletionStatus.OUTSTANDING
    ]
    return {"tasks": tasks}


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
    handler(environment_for(env), command)
    redirect(f"/{env}/add")


@route("/<env>/complete/<uuid_str>", method="POST")
def proc_complete_task(env: str, uuid_str: str):
    task_repo = environment_for(env).task_repository
    task = task_repo.retrieve_task_by_uuid(UUID(uuid_str))
    event = TaskCompletion(task, datetime.now())
    handler(environment_for(env), event)
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
