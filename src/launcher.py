from task.Task import Task
from task.TaskPriority import TaskPriority
from task.TaskCategory import TaskCategory
from _datetime import datetime
import json


myTask = Task.create_unfinished_task(
    'Simple Task',
    TaskPriority.URGENT_IMPORTANT,
    TaskCategory.PERSONAL,
    'Simple description',
    datetime.now(),
    datetime.now(),
    'Simple code to execute')

result = json.dumps(myTask.to_dict())
print(result)

simpleFile = open("simpleFile.json", 'w')
simpleFile.write(result)
simpleFile.close()
