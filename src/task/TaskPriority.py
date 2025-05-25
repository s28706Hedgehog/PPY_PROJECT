from enum import Enum


class Priority(Enum):
    URGENT_IMPORTANT = 1, 'UrgentImportant'
    NOT_URGENT_IMPORTANT = 2, 'NotUrgentImportant'
    URGENT_NOT_IMPORTANT = 3, 'UrgentNotImportant'
    NOT_URGENT_NOT_IMPORTANT = 4, 'NotUrgentNotImportant'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label
