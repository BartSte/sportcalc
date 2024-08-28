from argparse import ArgumentParser
from contextlib import suppress
from datetime import time


def make_parser() -> ArgumentParser:
    """
    Return the argument parser for the script.

    Returns
    -------
        The argument parser for the script

    """
    parser: ArgumentParser = ArgumentParser(
        description="Estimate the number of calories burned while cycling."
    )
    parser.add_argument(
        "weight_kg",
        action="store",
        type=float,
        help="Weight of the cyclist + bike in kg.",
    )

    parser.add_argument(
        "distance_km", action="store", type=float, help="Distance cycled in km."
    )

    parser.add_argument(
        "time",
        action="store",
        type=parse_time,
        help="The elapsed time as an iso format string (HH:MM:SS) or as a float"
        " representing the number of hours.",
    )

    parser.add_argument(
        "ascend_m",
        action="store",
        type=float,
        default=0,
        nargs="?",
        help="Total ascent in meters (default: 0).",
    )

    parser.add_argument(
        "descent_m",
        action="store",
        type=float,
        default=0,
        nargs="?",
        help="Total descent in meters (default: 0).",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Send the output as a JSON string to stdout.",
    )

    return parser


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
