from corecalc import exec
from corecalc.cli.parser import CoreParser

from speedskatingcalc.stats import SpeedSkatingStats


def main() -> str:
    """
    Entry point for the cyclingcalc module.

    Returns
    -------
        the summary of the cycling statistics.

    """
    return exec(CoreParser(), SpeedSkatingStats)


if __name__ == "__main__":
    print(main())
