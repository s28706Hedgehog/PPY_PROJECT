from enum import Enum


class TaskPriority(Enum):
    URGENT_IMPORTANT = 1, 'UrgentImportant'
    NOT_URGENT_IMPORTANT = 2, 'NotUrgentImportant'
    URGENT_NOT_IMPORTANT = 3, 'UrgentNotImportant'
    NOT_URGENT_NOT_IMPORTANT = 4, 'NotUrgentNotImportant'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label

    @staticmethod
    def get_task_priority(task_id: int):
        match task_id:
            case 1:
                return TaskPriority.URGENT_IMPORTANT
            case 2:
                return TaskPriority.NOT_URGENT_IMPORTANT
            case 3:
                return TaskPriority.URGENT_NOT_IMPORTANT
            case 4:
                return TaskPriority.NOT_URGENT_NOT_IMPORTANT
            case _d:
                return None
