from repositories.task_repository import TaskRepository, SQLiteTaskRepository
from objects.task import CompletionStatus

repo = SQLiteTaskRepository("tasks.db")

if __name__ == "__main__":
    active = [
        task
        for task in repo.get_all_tasks()
        if task.status == CompletionStatus.OUTSTANDING
    ]
    for ix, task in enumerate(active):
        print(f"{ix}: {task}")
