from datetime import datetime
from uuid import UUID

from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import CompletionStatus, Task
from repositories.helpers.helpers import mark_complete
from repositories.task_repository import TaskRepository, TextFileTaskRepository

repo = TextFileTaskRepository("task_list.txt")


@route("/")
def list_tasks(task_repository: TaskRepository = repo):
    return task_display(task_repository.get_all_tasks())

@route("/add")
def add_task(task_repository: TaskRepository = repo):
    return task_display(task_repository.get_all_tasks())

@route("/add", method="POST")
def proc_add_task(task_repository: TaskRepository = repo):
    description = request.forms.get('description')
    due = datetime.fromisoformat(request.forms.get('due')) if request.forms.get('due') else None
    task_repository.add_task(Task(description=description, due=due))
    redirect("/add")

@route("/complete", method="POST")
def proc_complete_task(task_repository: TaskRepository = repo):
    uuid_str = request.forms.get('uuid')
    mark_complete(task_repository, UUID(uuid_str))
    redirect("/add")

run(host="0.0.0.0", port=8000)
