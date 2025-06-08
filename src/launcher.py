from src.loader import JsonTaskLoader
from src.menu.MenuRefactor import ConsoleWindowManager, MainConsoleWindow

# TODO: Log system

tasks = JsonTaskLoader.load_all_tasks(r"C:\Users\jerzy\Desktop\TaskManager\rsc")
# menu = Menu(tasks)
# menu.show_menu(menu.main_options, menu.main_actions)

# ConsoleMenu.show_menu()

print("Tasks" + str(tasks))
window_manager = ConsoleWindowManager(tasks)
window_manager.add_new_window(MainConsoleWindow(tasks))
window_manager.show_current_window()

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
