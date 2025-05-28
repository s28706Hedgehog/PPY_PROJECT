from _datetime import datetime
from src.task.TaskCategory import TaskCategory
from src.task.TaskPriority import TaskPriority
from src.task.TaskState import TaskState
from src.task.TaskValidator import TaskValidator
import subprocess
import threading


def id_gen():
    curr = 1
    while True:
        yield curr
        curr += 1


_id_generator = id_gen()
_id_registry = set()


class Task:
    __slots__ = ['id', 'name', 'state', 'priority', 'category', 'description', 'beginDate', 'finishDate',
                 'deadlineDate',
                 'command', 'commandThread', 'commandProcess']
    id: int
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
        self.id = Task._get_available_id()
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
    def _get_available_id(cls):
        while True:
            test_id = next(_id_generator)
            if not _id_registry.__contains__(test_id):
                _id_registry.add(test_id)
                break
        return test_id

    @classmethod
    def create_task(cls, name: str, state: TaskState, priority: TaskPriority, category: TaskCategory, description: str,
                    begin_date: datetime, finish_date: datetime, deadline_date: datetime, command: str):
        return cls(name, state, priority, category, description, begin_date, finish_date, deadline_date,
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
        print("Task: " + self.name + " started")
        self.commandThread.start()

    def __get_command_process(self):
        self.commandProcess = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               text=True, shell=True, encoding='utf-8', universal_newlines=True,
                                               errors='ignore')
        output, errors = self.commandProcess.communicate()
        print("Task name: " + self.name + "\nfinished work with output: ",
              '\n', output, '\n', errors, '\n\n')
        self.__finish_task()

    def __finish_task(self):
        self.finishDate = datetime.now()
        self.state = TaskState.FINISHED

    def terminate_task(self):
        TaskValidator.validate_terminate_task(self)
        if self.commandProcess:
            self.commandProcess.terminate()
            self.commandProcess.wait()  # await termination
        if self.commandThread:
            self.commandThread.join()
        self.finishDate = datetime.now()
        self.state = TaskState.TERMINATED

    def change_description(self, new_description: str):
        self.description = new_description

    def change_command(self, new_command: str):
        TaskValidator.validate_change_command(self)
        self.command = new_command

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'state': self.state.order, 'priority': self.priority.order,
                'category': self.category.order,
                'description': self.description,
                'beginDate': self.beginDate.isoformat() if self.beginDate else None,
                'finishDate': self.finishDate.isoformat() if self.finishDate else None,
                'deadlineDate': self.deadlineDate.isoformat(), 'command': self.command}

    def __str__(self):
        return (
            f"Task '{self.name}':\n"
            f"  Id: {self.id}\n"
            f"  State: {self.state}\n"
            f"  Priority: {self.priority}\n"
            f"  Category: {self.category}\n"
            f"  Description: {self.description}\n"
            f"  Begin datetime: {self.beginDate.isoformat() if self.beginDate else 'None'}\n"
            f"  Finish datetime: {self.finishDate.isoformat() if self.finishDate else 'None'}\n"
            f"  Deadline datetime: {self.deadlineDate.isoformat() if self.deadlineDate else 'None'}\n"
            f"  Command: {self.command}")
