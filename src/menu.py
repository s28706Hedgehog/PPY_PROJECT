from src.task.Task import Task, TaskPriority, TaskCategory, TaskState, TaskValidator
from _datetime import datetime
import os
from collections.abc import Callable
from src.task.TaskExceptions import InvalidStateChangeException, NotAllowedTaskOperationException, \
    CorruptedTaskDataException

_options_type = dict[int, str]
_actions_type = dict[int, Callable]


class Menu:
    __slots__ = ['tasks', 'task_options', 'main_options', 'all_tasks_options', 'task_actions', 'all_tasks_actions',
                 'main_actions']
    tasks: list[Task]
    task_options: _options_type
    main_options: _options_type
    all_tasks_options: _options_type
    task_actions: _actions_type
    main_actions: _actions_type
    all_tasks_actions: _actions_type

    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self.task_options = {0: "back", 1: "start task", 2: "terminate task", 3: "edit command",
                             4: "edit description"}
        self.main_options = {0: "quit", 1: "browse tasks", 2: "show statistics"}
        self.all_tasks_options = {0: "back to main window", 1: "add task", 2: "manage task"}

        self.main_actions = {0: self.handle_quit, 1: self.handle_browse_tasks}
        self.task_actions = {0: None, 1: self.handle_start_task, 2: self.handle_terminate_task,
                             3: self.handle_edit_command,
                             4: self.handle_edit_description}
        self.all_tasks_actions = {0: self.handle_main_options, 1: self.handle_add_task, 2: self.handle_manage_task}

    def show_menu(self, options: _options_type, actions: _actions_type, *args, **kwargs):
        while True:
            self.print_options(options)
            res = self.handle_user_input(options)
            if res is not None:
                self.clear_console()
                actions[res](*args, **kwargs)
                break

    def print_options(self, options: _options_type):
        for optionId, optionMess in options.items():
            print(f"Enter {optionId} to {optionMess}")

    def handle_user_input(self, options: _options_type) -> int | None:
        try:
            user_input = int(input("Action: "))
            if user_input in options.keys():
                return user_input
        except ValueError:
            pass
        Menu.clear_console()
        print(IllegalMenuInputException("My friend, please reconsider your life choices :D"))
        return None

    def handle_quit(self):
        print("Trying to terminate all the running tasks")
        for task in self.tasks:
            try:
                task.terminate_task()
            except CorruptedTaskDataException | InvalidStateChangeException as e:
                print("Failed to terminate task: " + str(task))
                print("Reason: " + e)
        print("Goodbye my spiky friend")
        exit(0)

    def handle_add_task(self):
        try:
            name = input("Enter task name: ")
            print("Allowed priorities: ")
            print(TaskPriority._member_names_)
            priority = TaskPriority[input("Enter priority: ")]
            print("Allowed categories: ")
            print(TaskCategory._member_names_)
            category = TaskCategory[input("Enter category: ")]
            description = input("Enter task description: ")
            print("Example date: '2025-05-28T03:41:45.672818'")
            deadline_str = input("Enter deadline date: ")
            deadline = datetime.fromisoformat(deadline_str)
            command = input("Enter task command: ")

            task = Task.create_unfinished_task(
                name=name,
                priority=priority,
                category=category,
                description=description,
                deadline_date=deadline,
                command=command
            )

            self.tasks.append(task)
            print("Task successfully added")
        except Exception as e:
            print(f"Failed to add task: {e}")

    def handle_browse_tasks(self):
        self.print_tasks()
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def print_tasks(self):
        for task in self.tasks:
            print('Name [', task.name, '] ID [', task.id, '] command [', task.command, ']', end='\n\n')

    def print_tasks_detailed(self):
        for task in self.tasks:
            print(task, end='\n\n')

    def handle_manage_task(self):
        while True:
            Menu.clear_console()
            for task in self.tasks:
                print(task)
            resTaskId = int(input("Enter id of task you want to manage "))
            for task in self.tasks:
                if task.id == resTaskId:
                    isValid = True
                    break
                else:
                    isValid = False
            if isValid:
                break
            else:
                print(IllegalMenuInputException("My friend, coop with me, it's so annoying to write this"))
        self.show_menu(self.task_options, self.task_actions, resTaskId)

    def handle_main_options(self):
        Menu.clear_console()
        self.show_menu(self.main_options, self.main_actions)

    def handle_start_task(self, task_id: int):
        res = self.find_task(task_id)
        if res is not None:
            res.start_task()
        self.clear_console()
        self.print_tasks()
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def handle_terminate_task(self, task_id: int):
        res = self.find_task(task_id)
        if res is not None:
            res.terminate_task()
        self.clear_console()
        self.print_tasks()
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def handle_edit_command(self, task_id: int):
        res = self.find_task(task_id)
        if res is not None:
            new_command = input("Enter new command")
            res.change_command(new_command)
        self.clear_console()
        self.print_tasks()
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def handle_edit_description(self, task_id: int):
        res = self.find_task(task_id)
        if res is not None:
            new_description = input("Enter new description")
            res.change_description(new_description)
        self.clear_console()
        self.print_tasks()
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def find_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task_id == task.id:
                return task
        else:
            print(TaskNotFoundException("DAMMIT, enter proper task id"))
        return None

    @classmethod
    def clear_console(cls):
        print(1 * '\n')


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
