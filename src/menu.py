from src.task.Task import Task
import os


class Menu:
    __slots__ = ['tasks']
    tasks: list[Task]

    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def show_menu(self, options: dict[int, str]):
        pass

    def clear_console(self):
        print(100 * '\n')
