from src.loader import JsonTaskLoader
from src.menu.MenuRefactor import ConsoleWindowManager, MainConsoleWindow

tasks = JsonTaskLoader.load_all_tasks(r"C:\Users\jerzy\Desktop\TaskManager\rsc")

print("Tasks" + str(tasks))
window_manager = ConsoleWindowManager(tasks)
window_manager.add_new_window(MainConsoleWindow(tasks))
window_manager.show_current_window()

"""
    1. Adding new tasks ( both loading from files and hand written )
    2. Removing / editing Tasks
    3. Marking tasks as finished
    4. Print all task data ( specified task? )
    5. Print list of tasks ( all data but without description )
    6. Sort tasks by: name, priority, due date ( asc / desc ), state ( asc / desc )
    7. Filter tasks: task_priority, due_date(today, this week, this month), category, task_state
    8. Save / loading to file
    9. Generating statistics with charts ( average working time, % of tasks done on time, most frequent category )
    10. Handling exceptions ( minimum 10 )
    11. Simple interface
"""
