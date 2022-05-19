from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import Optional


class CompletionStatus(Enum):
    OTHER = 0
    OUTSTANDING = 1
    COMPLETED = 2
    WONT_DO = 3


@dataclass(frozen=True)
class Task:
    description: str
    due: Optional[datetime] = None
    status: CompletionStatus = CompletionStatus.OUTSTANDING

    def _due_description(self):
        return '' if self.due is None else self.due.isoformat()

    def _completion_status_description(self):
        return self.status.name

    def __str__(self):
        return f"{self.description}: {self._due_description()} ({self._completion_status_description})"
