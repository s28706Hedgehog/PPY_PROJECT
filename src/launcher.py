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
