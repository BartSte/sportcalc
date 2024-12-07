from sportcalc.core import exec

from sportcalc.implementations.cycling.parser import CyclingParser
from sportcalc.implementations.cycling.stats import CyclingStats


def main() -> str:
    """
    Entry point for the cyclingcalc module.

    Returns
    -------
        the summary of the cycling statistics.

    """
    return exec(CyclingParser(), CyclingStats)


if __name__ == "__main__":
    print(main())
