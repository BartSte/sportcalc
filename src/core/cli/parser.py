from argparse import ArgumentParser

from core.cli.type_parsers import parse_time


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

    return parser
