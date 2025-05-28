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

    # main_options -> all_tasks_options -> task_options
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self.task_options = {0: "back", 1: "start task", 2: "terminate task", 3: "edit command",
                             4: "edit description"}
        self.main_options = {0: "quit", 1: "browse tasks", 2: "show statistics"}
        self.all_tasks_options = {0: "back", 1: "add task", 2: "manage task", 3: "back to main window"}

        self.main_actions = {0: self.handle_quit, 1: self.handle_browse_tasks}
        self.task_actions = {0: None}
        self.all_tasks_actions = {0: None, 1: self.handle_add_task, 2: None,
                                  3: self.show_menu}

    def show_menu(self, options: _options_type, actions: _actions_type, *args, **kwargs):
        while True:
            self.print_options(options)
            res = self.handle_user_input(options)
            if res is not None:
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
        self.show_menu(self.all_tasks_options, self.all_tasks_actions)

    def handle_manage_task(self):
        while True:
            Menu.clear_console()
            for task in self.tasks:
                print(task)
            resTaskId = int(input("Enter id of task you want to manage"))
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

    @classmethod
    def clear_console(cls):
        # print(100 * '\n')
        print("\n")


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
