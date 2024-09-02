import json
from argparse import ArgumentParser, Namespace
from typing import Any

from running.cli.parser import make_parser
from running.cli.printer import print_summary
from running.stats import RunningStats


def main() -> str:
    """
    Return cycling statistics based on the cli arguments.

    Returns
    -------
        The cycling statistics based on the cli arguments

    """
    parser: ArgumentParser = make_parser()
    args: Namespace = parser.parse_args()

    result: RunningStats = RunningStats()

    # kwargs: dict[str, Any] = result.as_dict()
    # if args.json:
    #     kwargs["time"] = kwargs["time"].strftime("%H:%M:%S")
    #     return json.dumps(kwargs, indent=4)
    # else:
    #     return print_summary(kwargs)


if __name__ == "__main__":
    print(main())

