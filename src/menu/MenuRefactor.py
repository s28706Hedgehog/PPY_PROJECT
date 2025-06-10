from collections.abc import Callable
from src.task.TaskExceptions import InvalidStateChangeException, NotAllowedTaskOperationException, \
    CorruptedTaskDataException
from src.task.Task import Task
from enum import Enum
from typing import Optional


class ActionResultTypeEnum(Enum):
    DO_NOTHING = 1,
    SHOW_NEXT = 2
    SHOW_PREVIOUS = 3,
    QUIT = 4,


class ActionResult:
    __slots__ = ['action_result_type', 'next_window']
    action_result_type: ActionResultTypeEnum
    next_window: Optional['ConsoleWindowAbstract']

    def __init__(self, action: ActionResultTypeEnum, next_window: Optional['ConsoleWindowAbstract']):
        self.action_result_type = action
        self.next_window = next_window


_options_type = dict[int, str]
_actions_type = dict[int, Callable[..., ActionResult]]


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


class ConsoleWindowParamAbstract(ConsoleWindowAbstract):
    __slots__ = ['var_tuple', 'var_dict']

    def __init__(self, options: _options_type, actions: _actions_type, *args, **kwargs):
        super().__init__(options, actions)
        self.var_tuple = args
        self.var_dict = kwargs


def clear_console():
    print(1 * '\n')


class ConsoleWindowManager:
    __slots__ = ['window_stack', 'tasks', 'master_options_reserved']
    window_stack: list[ConsoleWindowAbstract]
    tasks: list[Task]
    master_options_reserved: list[int]

    def __init__(self, tasks: list[Task]):
        self.window_stack = []
        self.tasks = tasks
        self.master_options_reserved = [0]

    def show_current_window(self):
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
                    clear_console()
                    action_result = None
                    if isinstance(window, ConsoleWindowAbstract):
                        action_result = window.actions[user_response]()  # That's so annoying to track
                    elif isinstance(window, ConsoleWindowParamAbstract):
                        action_result = window.actions[user_response](window.var_dict, window.var_tuple)
                    if action_result is not None:
                        match action_result.action_result_type:
                            case ActionResultTypeEnum.DO_NOTHING:
                                pass
                            case ActionResultTypeEnum.SHOW_NEXT:
                                self.window_stack.append(action_result.next_window)
                                self.show_current_window()
                            case ActionResultTypeEnum.SHOW_PREVIOUS:
                                self.window_stack.pop()
                                self.show_current_window()
                            case ActionResultTypeEnum.QUIT:
                                self.quit()
                            case _default:
                                raise UnsupportedOperationException
                    break
            else:
                clear_console()

        # TODO: Handle action result here

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
                    clear_console()
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

    def browse_tasks(self) -> ActionResult:
        self.print_tasks()
        while True:
            try:
                usr_input = int(input("Enter id of task you would like to use: "))
            except ValueError:
                raise ValueError("Text you entered is not an integer :/")
            for tsk in self.tasks:
                if tsk.id == usr_input:
                    selected_task = tsk
                    clear_console()
                    return ActionResult(ActionResultTypeEnum.SHOW_NEXT, TaskConsoleWindow(selected_task))
            else:
                raise TaskNotFoundException("You entered wrong task id, please try again")

    def print_tasks(self):
        for task in self.tasks:
            print('ID [', task.id, '], Name [', task.name, '], Command [', task.command, ']', end='\n\n')


class TaskConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['selected_task']
    selected_task: Task

    def __init__(self, task: Task):
        super().__init__(
            {1: "start task", 2: "terminate task", 3: "edit command",
             4: "edit description"},
            {1: self.start_task, 2: self.terminate_task, 3: self.edit_command, 4: self.edit_description}
        )
        self.selected_task = task

    def start_task(self) -> ActionResult:
        self.selected_task.start_task()
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)

    def terminate_task(self) -> ActionResult:
        self.selected_task.terminate_task()
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)

    def edit_command(self) -> ActionResult:
        # Ik, no validation. But to be fair, I would kms before validating executable commands
        print("""Suggested command ( Telnet enabled required ):
        telnet telehack.com
        starwars
        """)
        new_command = input("Enter new command ( highly not recommended to do id manually :D ) ")
        self.selected_task.change_command(new_command)
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)

    def edit_description(self) -> ActionResult:
        new_description = input("Enter new description: ")
        self.selected_task.change_description(new_description)
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnsupportedOperationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
