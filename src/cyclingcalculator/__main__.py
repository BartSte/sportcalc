from argparse import ArgumentParser, Namespace

from cyclingcalculator.cli import make_parser
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

    result: CyclingStats = CyclingStats(
        time=args.time,
        distance_m=args.distance_km * 1000,
        weight_kg=args.weight_kg,
        ascend_m=args.ascend_m,
        descent_m=args.descent_m,
    )
    command = "json" if args.json else "summary"
    return getattr(result, command)


if __name__ == "__main__":
    print(main())
