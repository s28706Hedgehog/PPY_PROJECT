from enum import Enum


class TaskCategory(Enum):
    WORK = 1, 'work'
    PERSONAL = 2, 'personal'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label

    @staticmethod
    def get_task_category(task_id: int):
        match task_id:
            case 1:
                return TaskCategory.WORK
            case 2:
                return TaskCategory.PERSONAL
            case _d:
                return None
