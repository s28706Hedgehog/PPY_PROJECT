from src.task.TaskState import TaskState
from src.task.TaskExceptions import InvalidStateChangeException, CorruptedTaskDataException, \
    NotAllowedTaskOperationException


class TaskValidator:
    @classmethod
    def validate_start_task(cls, task: 'Task'):
        if task.state is TaskState.FINISHED:
            print(InvalidStateChangeException(
                "Can't start a task that's already finished. Consider creating a new task."))
        if task.state is TaskState.IN_PROGRESS:
            print(InvalidStateChangeException("Can't start a task that's already running."))
        if task.state is TaskState.TERMINATED:
            print(InvalidStateChangeException("Can't start a task that has already been terminated"))

    @classmethod
    def validate_terminate_task(cls, task: 'Task'):
        if task.state is TaskState.FINISHED:
            print(InvalidStateChangeException("Can't terminate task that's already finished."))
        if task.state is TaskState.TO_DO:
            print(InvalidStateChangeException("Can't terminate task that is not even running. Start it first"))
        if task.finishDate is not None:
            print(CorruptedTaskDataException(
                "Can't terminate task that already has a finish date. "
                "The task should either already be terminated or should not have a finish date."))
        # idk why it does not recognise
        # task.commandProcess.poll()

    @classmethod
    def validate_change_command(cls, task: 'Task'):
        if task.state is TaskState.IN_PROGRESS:
            print(NotAllowedTaskOperationException(
                "Can't modify task's command while it is running. Pause task first."))

    @classmethod
    def validate_pause_task(cls, task: 'Task'):
        if task.state is TaskState.TERMINATED:
            print(InvalidStateChangeException("Can't pause a task that has already been terminated"))
        if task.state is TaskState.FINISHED:
            print(InvalidStateChangeException("Can't pause a task that has already been finished"))
        if task.state is TaskState.TO_DO:
            print(InvalidStateChangeException("Can't pause a task that hasn't been started yet"))
