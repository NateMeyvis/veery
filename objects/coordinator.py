from abc import ABC, abstractmethod

class Event(Enum):
    pass

class TaskCompletion(Event):
    pass

class TaskCoordinator(ABC):

    @abstractmethod
    def proc_event(event: Event):
        raise NotImplementedError

