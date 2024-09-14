from corecalc import exec

from cyclingcalc.parser import CyclingParser
from cyclingcalc.stats import CyclingStats


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
