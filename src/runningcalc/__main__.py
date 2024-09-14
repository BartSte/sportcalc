from corecalc import exec

from runningcalc.parser import RunningParser
from runningcalc.stats import RunningStats


def main() -> str:
    """
    Entry point for the runningcalc module.

    Returns
    -------
        the summary of the runningcalc statistics.

    """
    return exec(RunningParser(), RunningStats)


if __name__ == "__main__":
    print(main())
