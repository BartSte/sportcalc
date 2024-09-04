from core import exec

from cycling.parser import CyclingParser
from cycling.stats import CyclingStats


def main() -> str:
    """
    Entry point for the cycling module.

    Returns
    -------
        the summary of the cycling statistics.

    """
    return exec(CyclingParser(), CyclingStats)


if __name__ == "__main__":
    print(main())
