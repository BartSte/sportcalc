from core.cli.parser import CoreParser
from core.cli.type_parsers import parse_percentage


def make_parser() -> CoreParser:
    """
    Return the argument parser for the script.

    Returns
    -------
        The argument parser for the script

    """
    parser: CoreParser = CoreParser(
        description="Calculate the energy consumption while cycling."
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

    return parser
