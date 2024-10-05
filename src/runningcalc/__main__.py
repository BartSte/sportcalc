from corecalc import exec
from corecalc.cli.parser import CoreParser

from runningcalc.stats import RunningStats


def main() -> str:
    """
    Entry point for the runningcalc module.

    Returns
    -------
        the summary of the runningcalc statistics.

    """
    return exec(CoreParser(), RunningStats)


if __name__ == "__main__":
    print(main())
