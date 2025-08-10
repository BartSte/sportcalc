import sys
from argparse import ArgumentParser
from collections.abc import Callable

from sportcalc import cycling, running, speedskating, walking

MainFunction = Callable[[list[str] | None], str]

ENTRY_POINTS: dict[str, MainFunction] = {
    "cycling": cycling.main,
    "running": running.main,
    "speedskating": speedskating.main,
    "walking": walking.main,
}


def main() -> str:
    """Run the sportcalc CLI dispatcher.

    Parses command-line arguments and dispatches to the selected sport module's
    main function. Prints the result and exits with status 1 when no valid
    sport is provided.
    """
    parser = ArgumentParser(
        prog="sportcalc",
        description="Calculate the energy consumption for various sports.",
        add_help=False,
    )
    parser.add_argument(
        "sport",
        choices=ENTRY_POINTS.keys(),
        nargs="?",
        help="The name of the sport to calculate the energy consumption for.",
    )
    parser.add_argument(
        "-h", "--help", action="store_true", help="Show help message"
    )
    args, _ = parser.parse_known_args()
    main: MainFunction | None = ENTRY_POINTS.get(args.sport)
    return main(sys.argv[2:]) if main else parser.format_help()


if __name__ == "__main__":
    print(main())
