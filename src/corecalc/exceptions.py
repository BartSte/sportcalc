class CoreException(Exception):
    """
    Base class for all exceptions in CoreCalc. Inherit from this class to
    if you want an exception to be logged as an error instead of critical.
    """


class CoreValueError(CoreException):
    """
    Exception raised when a value is invalid.
    """
