from src.task.Task import Task
from src.task.TaskState import TaskState
from src.task.TaskExceptions import InvalidStateChangeException, CorruptedTaskDataException, \
    NotAllowedTaskOperationException


class TaskValidator:
    @classmethod
    def validate_start_task(cls, task: Task):
        if task.state is TaskState.FINISHED:
            raise InvalidStateChangeException(
                "Can't start a task that's already finished. Consider creating a new task.")
        if task.state is TaskState.IN_PROGRESS:
            raise InvalidStateChangeException("Can't start a task that's already running.")
        if task.state is TaskState.TERMINATED:
            raise InvalidStateChangeException("Can't start a task that has already been terminated")

    @classmethod
    def validate_finish_task(cls, task: Task):
        if task.state is TaskState.FINISHED:
            raise InvalidStateChangeException("Can't finish task that's already finished.")
        if task.state is TaskState.TERMINATED:
            raise InvalidStateChangeException("Can't finish task that has already been terminated")
        if task.finishDate is not None:
            raise CorruptedTaskDataException(
                "Can't finish task that already has a finish date. "
                "The task should either already be finished or should not have a finish date.")

    @classmethod
    def validate_change_command(cls, task: Task):
        if task.state is TaskState.IN_PROGRESS:
            raise NotAllowedTaskOperationException(
                "Can't modify task's command while it is running. Pause task first.")

    @classmethod
    def validate_pause_task(cls, task: Task):
        if task.state is TaskState.TERMINATED:
            raise InvalidStateChangeException("Can't pause a task that has already been terminated")
        if task.state is TaskState.FINISHED:
            raise InvalidStateChangeException("Can't pause a task that has already been finished")
        if task is TaskState.TO_DO:
            raise InvalidStateChangeException("Can't pause a task that hasn't been started yet")
