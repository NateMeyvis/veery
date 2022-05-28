from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
    created: datetime = field(default_factory=datetime.now)
    uuid: UUID = field(default_factory=uuid4)

    @property
    def overdue(self):
        return self.due and (self.due < datetime.now())

    @property
    def stale(self):
        return not self.due and (datetime.now() - self.created).days >= 7

    def _due_description(self):
        return (
            "No due date"
            if self.due is None
            else f"Due {self.due.strftime('%m/%d/%Y')}"
        )

    def _completion_status_description(self):
        return self.status.name

    def _description_stub(self):
        return self.description[:10]

    def __str__(self):
        return f"{self.description}: {self._due_description()}"

    def kick(self, duration=timedelta(days=1)):
        """Add <duration> to the time to complete the task;
        if the task currently has no due date, or if the due date
        is in the past, make it <duration> from now."""
        if not self.due or self.due < datetime.now():
            self.due = datetime.now() + duration
        else:
            self.due += duration

    def __eq__(self, other):
        return all(
            [
                self.uuid == other.uuid,
                self.status == other.status,
                self.due == other.due,
                self.description == other.description,
            ]
        )
