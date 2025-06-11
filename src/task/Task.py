from _datetime import datetime
from src.task.TaskCategory import TaskCategory
from src.task.TaskPriority import TaskPriority
from src.task.TaskState import TaskState
from src.task.TaskValidator import TaskValidator
import subprocess
import threading
import os


def task_id_gen():
    curr = 1
    while True:
        yield curr
        curr += 1


def log_id_gen():
    curr = 1
    while True:
        yield curr
        curr += 1


class Logger:
    _id_generator = log_id_gen()
    _fileio_lock = threading.Lock()
    _log_file_name = 'logs' + str(datetime.now().isoformat().replace(':', '-')) + '.txt'

    @classmethod
    def log(cls, log_msg: str):
        with cls._fileio_lock:
            with open(cls._log_file_name, 'a') as file:
                file.write("Log: " + str(next(cls._id_generator)) + " " + str(datetime.now()) + "\n")
                file.write(log_msg + "\n\n")


_id_generator = task_id_gen()
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
        Logger.log("Task name: " + self.name + "\nfinished work with output: " + output + errors)
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

    def get_field_by_name(self, field_name: str):
        match field_name:
            case 'id':
                return self.id
            case 'name':
                return self.name
            case 'state':
                return self.state
            case 'priority':
                return self.priority
            case 'category':
                return self.category
            case 'description':
                return self.description
            case 'beginDate':
                return self.beginDate
            case 'finishDate':
                return self.finishDate
            case 'deadlineDate':
                return self.deadlineDate
            case 'command':
                return self.command
            case 'commandThread':
                return self.commandThread
            case 'commandProcess':
                return self.commandProcess
            case _d:
                return str(FieldNotFoundException(f"Class Task does not have field '{field_name}'"))

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


class FieldNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
