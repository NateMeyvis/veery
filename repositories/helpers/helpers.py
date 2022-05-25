from uuid import UUID

from repositories.task_repository import TaskRepository

from objects.task import CompletionStatus


def mark_complete(repository: TaskRepository, uuid: UUID):
    task_to_modify = repository.retrieve_task_by_uuid(uuid)
    repository.remove_task(task_to_modify)
    task_to_modify.status = CompletionStatus.COMPLETED
    repository.add_task(task_to_modify)
