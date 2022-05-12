from dataclasses import dataclass
from datetime import datetime

from typing import Optional


@dataclass(frozen=True)
class Task:
    description: str
    due: Optional[datetime] = None

    def __str__(self):
        return self.description

    @staticmethod
    def from_string(raw_string: str):
        return Task(description=raw_string)
