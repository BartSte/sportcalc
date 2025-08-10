from sportcalc._core import exec
from sportcalc._core.cli.parser import SportParser
from sportcalc._core.stats import MetsSpeedStats


class RunningStats(MetsSpeedStats):
    """Statistics for a running exercise.

    The MET values per speed were obtained from the following document:

        - https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pd

    I comapered the results with the following calculator:

        - TODO
    """

    METS_KM_H: tuple[float, ...] = (8.0, 9.6, 10.7, 12.0, 13.8, 16.1)
    METS_KCAL_KG_H: tuple[float, ...] = (8.0, 10.0, 11.0, 12.5, 14.0, 16.0)


def main(argv: list[str] | None = None) -> str:
    """Entry point for the running calculator.

    Args:
        argv: Optional list of command-line arguments.

    Returns:
        Result string produced by executing the RunningStats CLI.
    """
    return exec(SportParser(argv=argv), RunningStats)


if __name__ == "__main__":
    print(main())
