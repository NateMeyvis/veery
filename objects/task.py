from dataclasses import dataclass
from datetime import datetime

from typing import Optional

@dataclass
class Task:
    description: str
    due: Optional[datetime] = None
