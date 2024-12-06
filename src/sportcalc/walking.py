from sportcalc.core import exec
from sportcalc.core.cli.parser import CoreParser
from sportcalc.core.stats import MetsSpeedStats


class WalkingStats(MetsSpeedStats):
    """
    Statistics for a walking exercise.

    TODO: here mets values are available for walking on hills:
        https://pacompendium.com/walking/
    """

    METS_KM_H: tuple[float, ...] = 1.61, 3.22, 4.83, 5.68, 6.44
    METS_KCAL_KG_H: tuple[float, ...] = 2.0, 2.5, 3.3, 3.8, 5.0

def main() -> str:
    """
    Entry point for the runningcalc module.

    Returns
    -------
        the summary of the runningcalc statistics.

    """
    return exec(CoreParser(), WalkingStats)


if __name__ == "__main__":
    print(main())
