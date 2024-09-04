import json
from argparse import Namespace
from typing import Any

from core.cli.parser import CoreParser
from core.cli.printer import dump_json
from cycling.cli.parser import make_parser
from cycling.cli.printer import print_summary
from cycling.stats import CyclingStats


def main() -> str:
    """
    Return cycling statistics based on the cli arguments.

    Returns
    -------
        The cycling statistics based on the cli arguments

    """
    parser: CoreParser = make_parser()
    args: Namespace = parser.parse_args()

    distance_m: float = args.distance_km * 1000
    fraction_spend_drafting: float = args.drafting * 0.01
    result: CyclingStats = CyclingStats(
        time=args.time,
        distance_m=distance_m,
        weight_kg=args.weight_kg,
        ascend_m=args.ascend_m,
        descent_m=args.descent_m,
        fraction_spend_drafting=fraction_spend_drafting,
    )

    if args.json:
        return dump_json(result)
    else:
        return print_summary(result)


if __name__ == "__main__":
    print(main())
