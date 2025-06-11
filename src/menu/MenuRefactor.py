from _datetime import datetime
from collections.abc import Callable
from src.task.TaskExceptions import InvalidStateChangeException, \
    CorruptedTaskDataException
from src.task.Task import Task, TaskState, TaskPriority, TaskCategory
from enum import Enum
from typing import Optional
import matplotlib.pyplot as plt
from collections import defaultdict


class MenuSettings:
    __slots__ = ['task_filter', 'task_filter_allowed', 'task_sort', 'task_sort_allowed', 'task_print',
                 'task_print_allowed', 'sort_ascending']
    task_filter: dict[str: list]
    task_filter_allowed: list[str]
    task_sort: str
    task_sort_allowed: list[str]
    task_print: list[str]
    task_print_allowed: list[str]
    sort_ascending: bool

    def __init__(self):
        self.task_print_allowed = ['id', 'name', 'state', 'priority', 'category', 'description', 'beginDate',
                                   'finishDate', 'deadlineDate', 'command', 'commandThread', 'commandProcess']
        self.task_print = ['id', 'name', 'command', 'state']
        self.task_sort_allowed = ['id', 'name', 'state', 'priority', 'category', 'beginDate', 'finishDate',
                                  'deadlineDate']
        self.task_sort = 'id'
        self.sort_ascending = True

        self.task_filter = {}
        self.task_filter_allowed = ['id', 'name', 'state', 'priority', 'category', 'deadlineDate']

    def get_task_print_msg(self, task: Task) -> str:
        msg_list = []
        for i in range(0, len(self.task_print_allowed)):
            field_name = self.task_print_allowed[i]
            if self.task_print.__contains__(field_name):
                msg_list.append(field_name)
                msg_list.append(' [')
                msg_list.append(str(task.get_field_by_name(field_name)))
                msg_list.append('], ')

        return ''.join(msg_list)

    def get_tasks_print_msg(self, tasks: list[Task]) -> str:
        tsk_msg_list = []
        for tsk in tasks:
            tsk_msg_list.append(self.get_task_print_msg(tsk))
            tsk_msg_list.append('\n\n')
        return ''.join(tsk_msg_list)

    def remove_filter(self, flt: str):
        pass

    def add_filter(self, flt: str):
        pass

    def change_sort(self, srt: str):
        if srt in self.task_sort_allowed:
            self.task_sort = srt
            return
        raise WrongSettingException("Failed to change sort option")

    def change_sort_direction(self):
        self.sort_ascending = not self.sort_ascending

    def add_print(self, prt: str):
        if not self.task_print.__contains__(prt):
            if self.task_print_allowed.__contains__(prt):
                self.task_print.append(prt)
                return
        raise WrongSettingException("Failed to add print option")

    def remove_print(self, prt: str):
        if self.task_print.__contains__(prt):
            self.task_print.remove(prt)
            return
        raise WrongSettingException("Failed to remove print option")


class WrongSettingException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ActionResultTypeEnum(Enum):
    DO_NOTHING = 1,
    SHOW_NEXT = 2
    SHOW_PREVIOUS = 3,
    QUIT = 4,
    SHOW_CURRENT = 5


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
                        # Relic of the past
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
                            case ActionResultTypeEnum.SHOW_CURRENT:
                                self.show_current_window()
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
            if task.state == TaskState.IN_PROGRESS:
                try:
                    task.terminate_task()
                except CorruptedTaskDataException | InvalidStateChangeException as e:
                    print("Failed to terminate task: " + str(task))
                    print("Reason: " + e)
        print("Goodbye my spiky friend")
        exit(0)


class MainConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['tasks', 'settings']
    tasks: list[Task]
    settings: MenuSettings

    def __init__(self, tasks: list[Task], settings: MenuSettings):
        super().__init__(
            {1: "browse tasks", 2: "show statistics"},
            {1: self.browse_tasks, 2: self.next_stats_window}
        )
        self.tasks = tasks
        self.settings = settings

    def print_tasks(self):
        print(self.settings.get_tasks_print_msg(self.tasks))

    def browse_tasks(self) -> ActionResult:
        self.print_tasks()
        return ActionResult(ActionResultTypeEnum.SHOW_NEXT, BrowseTasksConsoleWindow(self.tasks, self.settings))

    def next_stats_window(self):
        return ActionResult(ActionResultTypeEnum.SHOW_NEXT, StatisticsConsoleWindow(self.tasks))


class BrowseTasksConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['tasks', 'settings']
    tasks: list[Task]
    settings: MenuSettings

    def __init__(self, tasks: list[Task], settings: MenuSettings):
        super().__init__(
            {1: 'select task', 2: 'settings', 3: 'add task'},
            {1: self.select_task, 2: self.show_settings_menu, 3: self.add_task}
        )
        self.tasks = tasks
        self.settings = settings

    def show_settings_menu(self) -> ActionResult:
        return ActionResult(ActionResultTypeEnum.SHOW_NEXT, MenuSettingsConsoleWindow(self.settings))

    def add_task(self) -> ActionResult:
        print("Task creation, you may enter '0' to stop task creation")

        name_input = input('Enter task name: ')
        if name_input == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)
        tsk_name = name_input

        print("Allowed priorities: ")
        print(TaskPriority._member_names_)
        priority_input = input("Enter priority: ")
        if priority_input == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

        print("Allowed categories: ")
        print(TaskCategory._member_names_)
        category_input = input("Enter category: ")
        if category_input == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

        tsk_description = input("Enter task description: ")
        if tsk_description == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

        print("Example date '2025-05-28'")
        date_input = input("Enter task deadline date: ")
        if date_input == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

        print("Sample command: 'ping 127.0.0.1 -n 20'")
        tsk_command = input("Enter task command: ")
        if tsk_command == '0':
            return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

        try:
            new_task = Task.create_unfinished_task(
                name=tsk_name,
                priority=TaskPriority[priority_input],
                category=TaskCategory[category_input],
                description=tsk_description,
                deadline_date=datetime.fromisoformat(date_input),
                command=tsk_command
            )

            self.tasks.append(new_task)
            print("Task successfully added")
        except Exception as e:
            print(f"Failed to add task: {e}")
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def select_task(self) -> ActionResult:
        self.print_tasks()
        while True:
            try:
                usr_input = int(input("Enter id of task you would like to use: ( '0' to go back )"))
                if usr_input == 0:
                    return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)
            except ValueError:
                raise ValueError("Text you entered is not an integer :/")
            for tsk in self.tasks:
                if tsk.id == usr_input:
                    selected_task = tsk
                    clear_console()
                    return ActionResult(ActionResultTypeEnum.SHOW_NEXT, TaskConsoleWindow(selected_task))
            else:
                print(TaskNotFoundException("You entered wrong task id, please try again"))

    def print_tasks(self):
        for task in self.tasks:
            print('ID [', task.id, '], Name [', task.name, '], Command [', task.command, ']', ', State [',
                  task.state, ']', end='\n\n')


class MenuSettingsConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['settings']
    settings: MenuSettings

    def __init__(self, settings: MenuSettings):
        super().__init__(
            {1: 'add filter', 2: 'remove filter', 3: 'change sort', 4: 'change sort direction',
             5: 'add task print data', 6: 'remove task print data'},
            {1: self.not_implemented, 2: self.not_implemented, 3: self.not_implemented, 4: self.not_implemented,
             5: self.add_print_data, 6: self.remove_print_data}
        )
        self.settings = settings

    def not_implemented(self) -> ActionResult:
        print('Not implemented')
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def add_print_data(self) -> ActionResult:
        print('Data allowed to print: ' + str(self.settings.task_print_allowed))
        print('Currently turned on: ' + str(self.settings.task_print))
        usr_print = input("Enter data to be printed ( one from above, enter '0' to back ): ")
        try:
            self.settings.add_print(usr_print)
        except WrongSettingException as e:
            print("I hate writing this, enter proper data again [" + str(e) + ']')
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def remove_print_data(self) -> ActionResult:
        print('Data allowed to print: ' + str(self.settings.task_print_allowed))
        print('Currently turned on: ' + str(self.settings.task_print))
        usr_print = input("Enter data to be removed from printing ( one from above, enter '0' to back ): ")
        try:
            self.settings.remove_print(usr_print)
        except WrongSettingException as e:
            print("I hate writing this, enter proper data again [" + str(e) + ']')
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)


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
        print("Suggested command: ping 127.0.0.1 -n 20")
        # Ik, no validation. But to be fair, I would kms before validating executable commands
        new_command = input("Enter new command ( highly not recommended to do id manually :D ) ")
        self.selected_task.change_command(new_command)
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)

    def edit_description(self) -> ActionResult:
        new_description = input("Enter new description: ")
        self.selected_task.change_description(new_description)
        return ActionResult(ActionResultTypeEnum.SHOW_PREVIOUS, None)


class StatisticsConsoleWindow(ConsoleWindowAbstract):
    __slots__ = ['tasks']
    tasks: list[Task]

    def __init__(self, tasks: list[Task]):
        super().__init__(
            {1: 'generate category chart', 2: 'generate priority chart', 3: 'generate avg completion time chart'},
            {1: self.gen_category_chart, 2: self.gen_priority_chart, 3: self.gen_avg_complete_time_chart}
        )
        self.tasks = tasks

    def gen_category_chart(self) -> ActionResult:
        if self.tasks:
            cat_count_dict = self.count_categories()
            plt.bar(cat_count_dict.keys(), cat_count_dict.values())
            plt.xlabel('category')
            plt.ylabel('count')
            plt.title('Tasks grouped by category')
            plt.show()
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def count_categories(self) -> dict[str, int]:
        res = defaultdict(int)
        for tsk in self.tasks:
            res[str(tsk.category)] += 1
        return res

    def gen_priority_chart(self) -> ActionResult:
        if self.tasks:
            cat_count_dict = self.count_priorities()
            plt.bar(cat_count_dict.keys(), cat_count_dict.values())
            plt.xlabel('priority')
            plt.ylabel('count')
            plt.title('Tasks grouped by priority')
            plt.show()
        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def count_priorities(self) -> dict[str, int]:
        res = defaultdict(int)
        for tsk in self.tasks:
            res[str(tsk.priority)] += 1
        return res

    def gen_avg_complete_time_chart(self) -> ActionResult:
        if self.tasks:
            cat_count_dict = self.calc_complete_times()
            if cat_count_dict:
                plt.bar(cat_count_dict.keys(), cat_count_dict.values())
                plt.xlabel('task id')
                plt.ylabel('completion time ( microseconds )')
                plt.title('Time to complete task')
                plt.show()
            else:
                print(DataNotAvailableException("There's 0 tasks that finished / terminated"))

        return ActionResult(ActionResultTypeEnum.SHOW_CURRENT, None)

    def calc_complete_times(self) -> dict[str, int]:
        res = defaultdict(int)
        for tsk in self.tasks:
            if tsk.state == TaskState.FINISHED or tsk.state == TaskState.TERMINATED:
                res[str(tsk.id)] += (tsk.finishDate.date() - tsk.beginDate.date()).microseconds
        return res


class DataNotAvailableException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class IllegalMenuInputException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnsupportedOperationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
