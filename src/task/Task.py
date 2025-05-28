from _datetime import datetime
from src.task.TaskCategory import TaskCategory
from src.task.TaskPriority import TaskPriority
from src.task.TaskState import TaskState
from src.task.TaskValidator import TaskValidator
import subprocess
import threading


class Task:
    __slots__ = ['name', 'state', 'priority', 'category', 'description', 'beginDate', 'finishDate', 'deadlineDate',
                 'command', 'commandThread', 'commandProcess']
    name: str
    state: TaskState
    priority: TaskPriority
    category: TaskCategory
    description: str
    beginDate: datetime
    finishDate: datetime | None
    deadlineDate: datetime
    command: str
    commandThread: threading.Thread | None
    commandProcess: subprocess.Popen | None

    def __init__(self, name: str, state: TaskState, priority: TaskPriority, category: TaskCategory, description: str,
                 begin_date: datetime | None, finish_date: datetime | None, deadline_date: datetime, command: str):
        self.name = name
        self.state = state
        self.priority = priority
        self.category = category
        self.description = description
        self.beginDate = begin_date
        self.finishDate = finish_date
        self.deadlineDate = deadline_date
        self.command = command
        self.commandThread = None
        self.commandProcess = None

    @classmethod
    def create_finished_task(cls, name: str, priority: TaskPriority, category: TaskCategory, description: str,
                             begin_date: datetime, finish_date: datetime, deadline_date: datetime, command: str):
        return cls(name, TaskState.FINISHED, priority, category, description, begin_date, finish_date, deadline_date,
                   command)

    @classmethod
    def create_unfinished_task(cls, name: str, priority: TaskPriority, category: TaskCategory, description: str,
                               deadline_date: datetime, command: str):
        return cls(name, TaskState.TO_DO, priority, category, description, None, None, deadline_date, command)

    def start_task(self):
        TaskValidator.validate_start_task(self)
        self.state = TaskState.IN_PROGRESS
        self.beginDate = datetime.now()
        self.commandThread = threading.Thread(target=self.__get_command_process)
        self.commandThread.start()

    def __get_command_process(self):
        self.commandProcess = subprocess.Popen([self.command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               text=True, shell=True)
        output, errors = self.commandProcess.communicate()
        print("Output: ", output)
        self.__finish_task()

    def __finish_task(self):
        self.finishDate = datetime.now()
        self.state = TaskState.FINISHED

    def terminate_task(self):
        TaskValidator.validate_terminate_task(self)
        self.commandProcess.terminate()
        self.commandProcess.wait()  # await termination
        self.finishDate = datetime.now()
        self.commandThread.join()
        self.state = TaskState.TERMINATED

    def change_description(self, new_description: str):
        self.description = new_description

    def change_command(self, new_command: str):
        TaskValidator.validate_change_command(self)
        self.command = new_command

    def to_dict(self):
        return {'name': self.name, 'state': self.state.order, 'priority': self.priority.order,
                'category': self.category.order,
                'description': self.description,
                'beginDate': self.beginDate.isoformat() if self.beginDate else None,
                'finishDate': self.finishDate.isoformat() if self.finishDate else None,
                'deadlineDate': self.deadlineDate.isoformat(), 'command': self.command}
