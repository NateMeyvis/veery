from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from typing import Optional


class CompletionStatus(Enum):
    OTHER = 0
    OUTSTANDING = 1
    COMPLETED = 2
    WONT_DO = 3


@dataclass
class Task:
    description: str
    due: Optional[datetime] = None
    status: CompletionStatus = CompletionStatus.OUTSTANDING
    uuid: UUID = field(default_factory=uuid4)

    def _due_description(self):
        return 'No due date' if self.due is None else f"Due {self.due.isoformat()}"

    def _completion_status_description(self):
        return self.status.name

    def _description_stub(self):
        return self.description[:10]

    def __str__(self):
        return f"{self.description}: {self._due_description()} ({self.status.name})"

    def __eq__(self, other):
        return all(
            [self.uuid == other.uuid,
            self.status == other.status,
            self.due == other.due,
            self.description == other.description]
        )
