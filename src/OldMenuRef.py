from collections.abc import Callable
from src.task.TaskExceptions import InvalidStateChangeException, NotAllowedTaskOperationException, \
    CorruptedTaskDataException
from src.task.Task import Task

_options_type = dict[int, str]
_actions_type = dict[int, Callable]
_tasks: list[Task]


def set_tasks(tasks: list[Task]):
    global _tasks
    _tasks = tasks


def show_menu(self, options: _options_type, actions: _actions_type, *args, **kwargs):
    while True:
        self.print_master_options(options)
        res = self.get_user_input(options)
        if res is not None:
            self.clear_console()
            actions[res](*args, **kwargs)
            break


def print_options(options: _options_type):
    for optionId, optionMess in options.items():
        print(f"Enter {optionId} to {optionMess}")


def handle_user_input(options: _options_type) -> int | None:
    try:
        user_input = int(input("Action: "))
        if user_input in options.keys():
            return user_input
    except ValueError:
        pass
    clear_console()
    print(IllegalMenuInputException("My friend, please reconsider your life choices :D"))
    return None


def print_tasks_detailed(tasks: list[Task]):
    for task in tasks:
        print(task, end='\n\n')


def print_tasks():
    global _tasks
    for task in _tasks:
        print('Name [', task.name, '] ID [', task.id, '] command [', task.command, ']', end='\n\n')


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


def clear_console():
    print(1 * '\n')


def not_implemented():
    raise NotImplementedError("I forgot to add something, take care of it")


class TaskListView:
    __slots__ = ['all_tasks_options', 'all_tasks_actions']
    all_tasks_options: _options_type
    all_tasks_actions: _actions_type

    def __init__(self):
        self.all_tasks_options = {0: "back to main window", 1: "add task", 2: "manage task"}
        self.all_tasks_actions = {0: self.handle_main_options, 1: self.handle_add_task, 2: self.handle_manage_task}


class MainView:
    __slots__ = ['main_options', 'main_actions', 'task_list_view']
    main_options: _options_type
    main_actions: _actions_type
    task_list_view: TaskListView

    def __init__(self):
        self.main_actions = {0: handle_quit, 1: self.handle_browse_tasks, 2: not_implemented}
        self.main_options = {0: "quit", 1: "browse tasks", 2: "show statistics"}
        self.task_list_view = TaskListView()

    def handle_browse_tasks(self):
        print_tasks()
        show_menu(self.task_list_view.all_tasks_options, self.task_list_view.all_tasks_actions,
                  (self.main_options, self.main_actions))


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
