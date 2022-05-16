import pytest

from objects.task import Task

@pytest.fixture
def tasks():
    return [Task("Do a thing"), Task("do another thing"), Task("do yet another thing")]
