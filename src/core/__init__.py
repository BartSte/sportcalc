from argparse import Namespace

from core.cli.parser import ExerciseParser
from core.stats import ExerciseStats


def exec(parser: ExerciseParser, cls: type[ExerciseStats]) -> str:
    """
    Run the statistics of the exercise based on the cli arguments.

    Returns
    -------
        The summary of the exercise statistics.

    """
    args: Namespace = parser.parse_args()
    result: ExerciseStats = cls.from_dict(vars(args))
    return result.json(indent=4) if args.json else result.summarize()
