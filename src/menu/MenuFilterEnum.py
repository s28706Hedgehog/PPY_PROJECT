from enum import Enum


class MenuFilterEnum(Enum):
    WORK = 1, 'work'
    PERSONAL = 2, 'personal'

    def __str__(self):
        return self.value[1]

    def __init__(self, order: int, label: str):
        self.order = order
        self.label = label