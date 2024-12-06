from sportcalc.core import exec

from sportcalc.speedskating.parser import SpeedSkatingParser
from sportcalc.speedskating.stats import SpeedSkatingStats


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
