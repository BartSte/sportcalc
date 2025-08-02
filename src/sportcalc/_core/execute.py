import logging
import sys
from argparse import Namespace
from types import TracebackType

from sportcalc._core.cli.parser import CoreParser
from sportcalc._core.exceptions import CoreException
from sportcalc._core.stats import ExerciseStats


def exec(parser: CoreParser, cls: type[ExerciseStats]) -> str:
    """Run the statistics of the exercise based on the cli arguments.

    Returns
    -------
        The summary of the exercise statistics.

    """
    sys.excepthook = except_hook
    args: Namespace = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    logging.debug("Log level is set to %s", args.loglevel)
    logging.debug("Arguments: %s", args)
    logging.debug("Statistics type: %s", cls.__name__)

    result: ExerciseStats = cls(**vars(args))
    result.update()
    return result.json(indent=4) if args.json else result.summarize()


def except_hook(
    exctype: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> None:
    """Handle exceptions and log them.

    Args:
        exctype: the type of the exception.
        value: the exception instance.
        traceback: the traceback object.

    """
    known_exceptions: list[type[BaseException]] = [
        CoreException,
        KeyboardInterrupt,
    ]

    if any(isinstance(value, exception) for exception in known_exceptions):
        logging.error(f"{exctype.__name__}: {value}")
    else:
        logging.critical(
            f"{exctype.__name__}: {value}", exc_info=(exctype, value, traceback)
        )
