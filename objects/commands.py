from dataclasses import dataclass

from objects.task import Task


class Command:
    pass


@dataclass
class AddTask(Command):
    task: Task
