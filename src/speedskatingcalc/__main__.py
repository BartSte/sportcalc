from corecalc import exec

from speedskatingcalc.parser import SpeedSkatingParser
from speedskatingcalc.stats import SpeedSkatingStats


def main() -> str:
    """
    Entry point for the cyclingcalc module.

    Returns
    -------
        the summary of the cycling statistics.

    """
    return exec(SpeedSkatingParser(), SpeedSkatingStats)


if __name__ == "__main__":
    print(main())
