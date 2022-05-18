from bottle import redirect, request, route, run

from display.task_display import task_display
from objects.task import Task
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
    due = None
    task_repository.add_task(Task(description))
    redirect("/add")

run(host="0.0.0.0", port=8000)
