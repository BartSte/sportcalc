from core import exec

from running.parser import RunningParser
from running.stats import RunningStats


def main() -> str:
    """
    Entry point for the running module.

    Returns
    -------
        the summary of the running statistics.

    """
    return exec(RunningParser(), RunningStats)


if __name__ == "__main__":
    print(main())
