import TaskState
import TaskPriority
import TaskCategory
import datetime


class Task:
    __slots__ = ['name', 'state', 'priority', 'category', 'description', 'beginDate', 'finishDate']
    name: str
    state: TaskState
    priority: TaskPriority
    category: TaskCategory
    description: str
    beginDate: datetime
    finishDate: datetime

    def __init__(self, name: str, state: TaskState, priority: TaskPriority, category: TaskCategory, description: str,
                 begin_date: datetime, finish_date: datetime):
        self.name = name
        self.state = state
        self.priority = priority
        self.category = category
        self.description = description
        self.beginDate = begin_date
        self.finishDate = finish_date
