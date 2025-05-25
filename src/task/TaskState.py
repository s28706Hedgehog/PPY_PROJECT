from enum import Enum


class TaskState(Enum):
    TO_DO = 1, 'ToDo'
    IN_PROGRESS = 2, 'InProgress'
    PAUSED = 3, 'Paused'
    FINISHED = 4, 'Finished'
    TERMINATED = 5, 'Terminated'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label
