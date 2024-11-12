import logging
import re
from contextlib import suppress
from datetime import time

from corecalc.exceptions import CoreValueError

TIME_UNITS: dict[str, int] = {
    "h": 3600,
    "hour": 3600,
    "hours": 3600,
    "m": 60,
    "min": 60,
    "minute": 60,
    "minutes": 60,
    "s": 1,
    "sec": 1,
    "second": 1,
    "seconds": 1,
}


def parse_time(time_str: str) -> time:
    """Return the time as a time object.

    First, the time is parsed assuming the user provided the time with a unit.
    If this fails, the time is parsed as an iso format string.

    Arguments:
    ---------
        time_str: the time as a string

    Raises:
    ------
        CoreValueError: if the time cannot be parsed.

    Returns:
    -------
        the time as a time object

    """
    with suppress(ValueError):
        return parse_time_with_unit(time_str)

    try:
        return parse_iso_time(time_str)
    except ValueError as error:
        raise CoreValueError(
            "Invalid time format. It must be in iso format, a single float, or "
            "a float with a time unit."
        ) from error


def parse_time_with_unit(time_str: str) -> time:
    """Return the time as a time object.

    The minimal resolution is 1 second.

    Arguments:
    ---------
        time_str: the time as a string containing one of the following units:
            h/hour/hours, m/minute/minutes, s/second/seconds.

    Raises:
    ------
        ValueError: if the time cannot be parsed.

    Returns:
    -------
        the time as a time object

    """
    chars: str = re.sub(r"^[0-9,. ]*", "", time_str)
    numbers: str = re.sub(r"[a-zA-Z ]*$", "", time_str).replace(" ", "")
    logging.debug("Found chars: %s", chars)
    logging.debug("Found numbers: %s", numbers)
    try:
        unit: str = next(x for x in TIME_UNITS if numbers and x == chars)
    except StopIteration as error:
        raise ValueError(
            "Time must contain a unit. For example, 1 hour, 30 minutes, or 1 "
            "second."
        ) from error
    else:
        total_seconds: int = int(float(numbers) * TIME_UNITS[unit])
        return _seconds_to_time(total_seconds)


def _seconds_to_time(total_seconds: int) -> time:
    total_milliseconds: int = int(total_seconds * 1000)
    seconds, _ = divmod(total_milliseconds, 1000)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(hour=hours, minute=minutes, second=seconds)


def parse_iso_time(time_str: str) -> time:
    """Return the time as a time object.

    Arguments:
    ---------
        time_str: the time as a string

    Returns:
    -------
        the time as a time object

    """
    time_str = float_to_iso(time_str)
    return time.fromisoformat(time_str)


def float_to_iso(time_str: str) -> str:
    """If `time_str` can be converted to a float, it is converted to an iso format
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
    """Return the percentage as a float.

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
        raise CoreValueError(
            "Percentage must be a number. Decimals and a % sign is allowed."
        ) from error
    else:
        if not 0 <= percentage <= 100:
            raise CoreValueError("Percentage must be between 0 and 100.")

    return percentage
