from contextlib import suppress
from datetime import time


def parse_time(time_str: str) -> time:
    """
    Return the time as a time object.

    Arguments:
    ---------
        time_str: the time as a string

    Returns:
    -------
        the time as a time object

    """
    time_str = float_to_iso(time_str)
    try:
        return time.fromisoformat(time_str)
    except ValueError as error:
        msg: str = (
            "Time must be in iso format. For example, 01:30:00 is 1 hour and 30"
            " minutes."
        )
        raise ValueError(msg) from error


def float_to_iso(time_str: str) -> str:
    """
    If `time_str` can be converted to a float, it is converted to an iso format
    string. Otherwise, the original string is returned.

    Arguments:
    ---------
        time_str: the time as a string

    Returns:
    -------
        the time as a time object

    """
    with suppress(ValueError):
        hours = float(time_str)
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        seconds = int((hours - whole_hours - (minutes / 60)) * 3600)
        time_str = f"{whole_hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str


def parse_percentage(percentage: str | int | float) -> float:
    """
    Return the percentage as a float.

    Arguments:
    ---------
        percentage: the percentage as a string

    Returns:
    -------
        the percentage as a float

    """
    if isinstance(percentage, str):
        percentage = percentage.replace("%", "")

    try:
        percentage = float(percentage)
    except ValueError as error:
        raise ValueError(
            "Percentage must be a number. Decimals and a % sign is allowed."
        ) from error
    else:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")

    return percentage
