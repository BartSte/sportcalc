import logging
import sys
from argparse import Namespace
from types import TracebackType

from corecalc.cli.parser import ExerciseParser
from corecalc.stats import ExerciseStats


def exec(parser: ExerciseParser, cls: type[ExerciseStats]) -> str:
    """
    Run the statistics of the exercise based on the cli arguments.

    Returns
    -------
        The summary of the exercise statistics.

    """
    sys.excepthook = except_hook
    args: Namespace = parser.parse_args()
    result: ExerciseStats = cls.from_dict(vars(args))
    return result.json(indent=4) if args.json else result.summarize()


def except_hook(
    exctype: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> None:
    """
    Handle exceptions and log them.

    Args:
        exctype: the type of the exception.
        value: the exception instance.
        traceback: the traceback object.

    """
    known_exceptions: tuple[type[BaseException]] = tuple()

    if exctype in known_exceptions:
        logging.error(f"{exctype.__name__}: {value}")
    else:
        logging.critical(
            f"{exctype.__name__}: {value}", exc_info=(exctype, value, traceback)
        )
