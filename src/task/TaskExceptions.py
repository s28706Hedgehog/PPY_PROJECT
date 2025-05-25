class InvalidStateChangeException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CorruptedTaskDataException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NotAllowedTaskOperationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
