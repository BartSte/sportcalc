from argparse import Namespace

from core.stats import ExerciseStats

from cycling.cli import CyclingParser
from cycling.stats import CyclingStats


def main() -> str:
    """
    Return cycling statistics based on the cli arguments.

    Returns
    -------
        The cycling statistics based on the cli arguments

    """
    parser: CyclingParser = CyclingParser()
    args: Namespace = parser.parse_args()
    result: ExerciseStats = CyclingStats.from_dict(vars(args))
    return result.json(indent=4) if args.json else result.summarize()


if __name__ == "__main__":
    print(main())
