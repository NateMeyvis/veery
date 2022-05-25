from datetime import datetime

import pytest

from objects.task import Task


@pytest.fixture
def tasks():
    return [
        Task("Do a thing", due=datetime(2022, 1, 7, 2, 9)),
        Task("do another thing"),
        Task("do yet another thing", due=datetime(2022, 4, 2, 4, 2)),
    ]
