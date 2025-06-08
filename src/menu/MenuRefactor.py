from collections.abc import Callable
from src.task.TaskExceptions import InvalidStateChangeException, NotAllowedTaskOperationException, \
    CorruptedTaskDataException
from src.task.Task import Task

_options_type = dict[int, str]
_actions_type = dict[int, Callable]


class ConsoleWindowAbstract:
    """
    By window, I mean console menu that prints its options for user and handles all necessary actions
    """
    __slots__ = ['options', 'actions']
    options: _options_type
    actions: _actions_type

    def __init__(self, options: _options_type, actions: _actions_type):
        self.options = options
        self.actions = actions


class ConsoleWindowManager:
    __slots__ = ['window_stack', 'tasks', 'master_options_reserved']
    window_stack: list[ConsoleWindowAbstract]
    tasks: list[Task]
    master_options_reserved: list[int]

    def __init__(self, tasks: list[Task]):
        self.window_stack = []
        self.tasks = tasks
        self.master_options_reserved = [0]

    def show_current_window(self, *args, **kwargs):
        window = self.window_stack[-1]

        while True:
            self.print_master_options()
            self.print_options(window.options)
            user_response = self.get_user_input()
            if user_response is not None:
                if self.check_if_master_option(user_response):
                    self.master_user_input_handler(user_response, window)
                    break
                elif self.check_if_match_any_option(user_response, window.options):
                    self.clear_console()
                    window.actions[user_response](*args, **kwargs)
                    break

    def check_if_master_option(self, option: int):
        return option in self.master_options_reserved

    @staticmethod
    def check_if_match_any_option(option: int, options: _options_type):
        if option in options.keys():
            return True
        else:
            raise IllegalMenuInputException("My friend, please reconsider your life choices :D\n"
                                            "Not allowed number entered!")

    @staticmethod
    def get_user_input() -> int | None:
        try:
            user_input = int(input("Action: "))
            return user_input
        except ValueError:
            raise ValueError("Text you entered is not an integer :/")

    def master_user_input_handler(self, user_input: int, caller_window: ConsoleWindowAbstract):
        match user_input:
            case 0:
                if isinstance(caller_window, MainConsoleWindow):
                    self.quit()
                else:
                    self.show_previous_window()
            case _d:
                pass

    @staticmethod
    def print_options(options: _options_type):
        for optionId, optionMess in options.items():
            print(f"Enter {optionId} to {optionMess}")

    @staticmethod
    def print_master_options():
        print("Enter 0 to Back / Quit")

    def add_new_window(self, window: ConsoleWindowAbstract):
        self.window_stack.append(window)

    # CHECK if I can perform .pop ( empty list )
    def show_previous_window(self):
        self.window_stack.pop()
        self.show_current_window()

    @staticmethod
    def clear_console():
        print(1 * '\n')

    def quit(self):
        print("Trying to terminate all the running tasks")
        for task in self.tasks:
            try:
                task.terminate_task()
            except CorruptedTaskDataException | InvalidStateChangeException as e:
                print("Failed to terminate task: " + str(task))
                print("Reason: " + e)
        print("Goodbye my spiky friend")
        exit(0)


class MainConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['tasks_ref', 'tasks']
    tasks: list[Task]

    def __init__(self, tasks: list[Task]):
        super().__init__(
            {1: "browse tasks", 2: "show statistics"},
            {1: self.browse_tasks, 2: None}
        )
        self.tasks = tasks

    def browse_tasks(self):
        self.print_tasks()
        # show_menu()

    def print_tasks(self):
        for task in self.tasks:
            print('Name [', task.name, '] ID [', task.id, '] command [', task.command, ']', end='\n\n')


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
