from sportcalc._core import exec
from sportcalc._core.cli.parser import CoreParser
from sportcalc._core.stats import MetsSpeedStats


class WalkingStats(MetsSpeedStats):
    """
    Statistics for a walking exercise.

    TODO: here mets values are available for walking on hills:
        https://pacompendium.com/walking/
    """

    METS_KM_H: tuple[float, ...] = 1.61, 3.22, 4.83, 5.68, 6.44
    METS_KCAL_KG_H: tuple[float, ...] = 2.0, 2.5, 3.3, 3.8, 5.0

def main(argv: list[str] | None = None) -> str:
    """Entry point for the walking CLI.

    Args:
        argv: Optional list of command-line arguments.

    Returns:
        Result string produced by the core executor.
    """
    return exec(CoreParser(argv=argv), WalkingStats)


if __name__ == "__main__":
    print(main())
