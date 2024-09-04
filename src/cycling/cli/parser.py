from argparse import ArgumentParser

from core.cli.parser import make_parser as make_core_parser
from core.cli.type_parsers import parse_percentage


def make_parser() -> ArgumentParser:
    """
    Return the argument parser for the script.

    Returns
    -------
        The argument parser for the script

    """
    parser: ArgumentParser = make_core_parser()

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
