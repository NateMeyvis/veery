from typing import List

from objects.task import Task


class TaskRepository:
    def __init__(self, path: str):
        self._path = path

    @staticmethod
    def task_from_string(serialized: str) -> Task:
        return Task(description=serialized)

    @staticmethod
    def task_to_string(to_serialize: Task) -> str:
        return to_serialize.description

    def get_all_tasks(self):
        tasks = []
        with open(self._path) as f:
            for task_line in f.readlines():
                tasks.append(TaskRepository.task_from_string(task_line.strip()))
        return tasks

    def set_task_list(self, tasks: List[Task]):
        with open(self._path, "w") as f:
            f.write("\n".join([TaskRepository.task_to_string(task) for task in tasks]))

    def add_task(self, new_task: Task):
        task_list = self.get_all_tasks()
        task_list.append(new_task)
        self.set_task_list(task_list)

    def remove_task(self, task_to_remove: Task):
        task_list = self.get_all_tasks()
        task_list = [task for task in task_list if task != task_to_remove]
        self.set_task_list(task_list)
