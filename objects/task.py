from dataclasses import dataclass
from datetime import datetime

from typing import Optional


@dataclass(frozen=True)
class Task:
    description: str
    due: Optional[datetime] = None

    def __str__(self):
        return f"{self.description}: {'no due date' if self.due is None else self.due.isoformat()}"
