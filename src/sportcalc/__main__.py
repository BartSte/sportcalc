import sys
from argparse import Namespace

from sportcalc._core.cli.dispatch_parser import DispatchParser


def main() -> str:
    """Run the sportcalc CLI dispatcher.

    Parses command-line arguments and dispatches to the selected sport module's
    main function. Prints the result and exits with status 1 when no valid
    sport is provided.
    """
    parser = DispatchParser(
        prog="sportcalc",
        description="Calculate the energy consumption for various sports.",
    )
    args: Namespace = parser.parse_known_args()[0]
    return args.func(sys.argv[2:]) if args.func else parser.format_help()


if __name__ == "__main__":
    print(main())
