from enum import Enum


class TaskState(Enum):
    TO_DO = 1, 'ToDo'
    IN_PROGRESS = 2, 'InProgress'
    FINISHED = 3, 'Finished'
    TERMINATED = 4, 'Terminated'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label
