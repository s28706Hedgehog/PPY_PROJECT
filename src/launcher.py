from src.loader import JsonTaskLoader
from src.menu.MenuRefactor import ConsoleWindowManager, MainConsoleWindow, MenuSettings
from pathlib import Path

launcher_path = Path(__file__).resolve()
rsc_path = str(launcher_path.parent.parent) + r"\rsc"

tasks = JsonTaskLoader.load_all_tasks(rsc_path)

print("Tasks" + str(tasks))
window_manager = ConsoleWindowManager(tasks)
window_manager.add_new_window(MainConsoleWindow(tasks, MenuSettings()))
window_manager.show_current_window()

"""
TODO: ( Fixes, improvements, new features )
    1) Cleanup MenuRefactor module
    2) Handle exceptions properly
    3) Finish settings / options / filter
    4) Cleanup exceptions
    5) Optimise imports
    6) Check for return's of functions type annotations
    7) Fix task not being able to terminate
    8) Deadline validation ( or any kind of info, like FINISHED_AFTER_DEADLINE )
    9) Separate module for handling paths
    10) Small tweaks to display
"""