from argparse import ArgumentParser

from cyclingcalculator.cli.type_parsers import parse_percentage, parse_time


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
        "-d",
        "--drafting",
        action="store",
        type=parse_percentage,
        default=0,
        help="Percentage of time spent drafting behind another cyclist. 0 "
        "default, meaning no drafting. A value of 100 means you spent all your "
        "time drafting.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Send the output as a JSON string to stdout.",
    )

    return parser
