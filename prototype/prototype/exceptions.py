class GoalNotFoundError(RuntimeError):
    """
    Raised when a search could not find the goal position.
    """
    pass


class InvalidPathError(RuntimeError):
    """
    Raised when a path (goal sequence) is found to be invalid.
    """
    pass

