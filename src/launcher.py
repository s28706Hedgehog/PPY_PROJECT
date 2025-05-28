from _datetime import datetime
from src.task.Task import Task
from src.task.TaskPriority import TaskPriority
from src.task.TaskCategory import TaskCategory
import json
from src.task.TaskState import TaskState
from src.loader import JsonTaskLoader
from menu import Menu
import time

# TODO: Log system

tasks = JsonTaskLoader.load_all_tasks(r"C:\Users\jerzy\Desktop\PPY_Task_Manager\rsc")
menu = Menu(tasks)
menu.show_menu(menu.main_options, menu.main_actions)

"""
myTask = Task.create_unfinished_task(
    'Simple Task',
    TaskPriority.URGENT_IMPORTANT,
    TaskCategory.PERSONAL,
    'Simple description',
    datetime.now(),
    "python print('anything')")

myTask.start_task()
"""

"""
result = json.dumps(myTask.to_dict())
print(result)

simpleFile = open("simpleFile.json", 'w')
simpleFile.write(result)
simpleFile.close()
"""
