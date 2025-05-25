from _datetime import datetime

from src.task.TaskCategory import TaskCategory
from src.task.TaskExceptions import InvalidStateChangeException, CorruptedTaskDataException, \
    NotAllowedTaskOperationException
from src.task.TaskPriority import TaskPriority
from src.task.TaskState import TaskState


class Task:
    __slots__ = ['name', 'state', 'priority', 'category', 'description', 'beginDate', 'finishDate', 'deadlineDate',
                 'command']
    name: str
    state: TaskState
    priority: TaskPriority
    category: TaskCategory
    description: str
    beginDate: datetime
    finishDate: datetime | None
    deadlineDate: datetime
    command: str

    def __init__(self, name: str, state: TaskState, priority: TaskPriority, category: TaskCategory, description: str,
                 begin_date: datetime, finish_date: datetime | None, deadline_date: datetime, command: str):
        self.name = name
        self.state = state
        self.priority = priority
        self.category = category
        self.description = description
        self.beginDate = begin_date
        self.finishDate = finish_date
        self.deadlineDate = deadline_date
        self.command = command

    @classmethod
    def create_finished_task(cls, name: str, priority: TaskPriority, category: TaskCategory, description: str,
                             begin_date: datetime, finish_date: datetime, deadline_date: datetime, command: str):
        return cls(name, TaskState.FINISHED, priority, category, description, begin_date, finish_date, deadline_date,
                   command)

    @classmethod
    def create_unfinished_task(cls, name: str, priority: TaskPriority, category: TaskCategory, description: str,
                               begin_date: datetime, deadline_date: datetime, command: str):
        return cls(name, TaskState.TO_DO, priority, category, description, begin_date, None, deadline_date, command)

    def start_task(self):
        if self.state is TaskState.FINISHED:
            raise InvalidStateChangeException("Can't start task that's already finished, consider creating a new task.")
        if self.state is TaskState.IN_PROGRESS:
            raise InvalidStateChangeException("Can't start task that's already running.")
        self.state = TaskState.IN_PROGRESS

    def finish_task(self):
        if self.state is TaskState.FINISHED:
            raise InvalidStateChangeException("Can't finish task that's already finished.")

        if self.finishDate is not None:
            raise CorruptedTaskDataException(
                "Can't finish task that already has finish date. "
                "Task either should be already finished or it shouldn't have finishDate. ")
        self.finishDate = datetime.now()
        self.state = TaskState.FINISHED

    def change_description(self, new_description: str):
        self.description = new_description

    def change_command(self, new_command: str):
        if self.state is TaskState.IN_PROGRESS:
            raise NotAllowedTaskOperationException(
                "Can't modify task command while task is running. Stop task to change it's command.")
        self.command = new_command

    def to_dict(self):
        return {'name': self.name, 'state': self.state.order, 'priority': self.priority.order,
                'category': self.category.order,
                'description': self.description, 'beginDate': self.beginDate.isoformat(),
                'finishDate': self.finishDate.isoformat() if self.finishDate else None,
                'deadlineDate': self.deadlineDate.isoformat(), 'command': self.command}
