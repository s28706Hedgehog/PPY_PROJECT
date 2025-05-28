from _datetime import datetime
from src.task.Task import Task
from src.task.TaskPriority import TaskPriority
from src.task.TaskCategory import TaskCategory
import json
from src.task.TaskState import TaskState

myTask = Task.create_unfinished_task(
    'Simple Task',
    TaskPriority.URGENT_IMPORTANT,
    TaskCategory.PERSONAL,
    'Simple description',
    datetime.now(),
    "python print('anything')")

myTask.start_task()

"""
result = json.dumps(myTask.to_dict())
print(result)

simpleFile = open("simpleFile.json", 'w')
simpleFile.write(result)
simpleFile.close()
"""