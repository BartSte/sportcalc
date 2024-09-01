import json
from argparse import ArgumentParser, Namespace
from typing import Any

from cyclingcalculator.cli.parser import make_parser
from cyclingcalculator.cli.printer import print_summary
from cyclingcalculator.stats import CyclingStats


def main() -> str:
    """
    Return cycling statistics based on the cli arguments.

    Returns
    -------
        The cycling statistics based on the cli arguments

    """
    parser: ArgumentParser = make_parser()
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

    kwargs: dict[str, Any] = result.as_dict()
    if args.json:
        # TODO exclude non-SI from json
        # non_si_units: tuple[str, ...] = "kj", "kmph", "km"
        # exclude_non_si = [x for x in dir(self) if x.endswith(non_si_units)]
        # exclude.extend(exclude_non_si)
        # TODO make a serializer for time
        kwargs["time"] = kwargs["time"].strftime("%H:%M:%S")
        return json.dumps(kwargs, indent=4)
    else:
        return print_summary(kwargs)


if __name__ == "__main__":
    print(main())
