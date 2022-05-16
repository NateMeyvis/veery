from bottle import route, run
from display.task_display import task_display
from repositories.task_repository import TaskRepository, TextFileTaskRepository

repo = TextFileTaskRepository("task_list.txt")

@route("/")
def list_tasks(task_repository: TaskRepository = repo):
    return task_display(task_repository.get_all_tasks())

run(host="0.0.0.0", port=8000)
