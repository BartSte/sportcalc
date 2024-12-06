from sportcalc.core import exec
from sportcalc.core.cli.parser import CoreParser
from sportcalc.core.stats import MetsSpeedStats


class RunningStats(MetsSpeedStats):
    """Statistics for a running exercise.

    The MET values per speed were obtained from the following document:

        - https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pd

    I comapered the results with the following calculator:

        - TODO
    """

    METS_KM_H: tuple[float, ...] = (8.0, 9.6, 10.7, 12.0, 13.8, 16.1)
    METS_KCAL_KG_H: tuple[float, ...] = (8.0, 10.0, 11.0, 12.5, 14.0, 16.0)


def main() -> str:
    """Entry point for the runningcalc module.

    Returns
    -------
        the summary of the runningcalc statistics.

    """
    return exec(CoreParser(), RunningStats)


if __name__ == "__main__":
    print(main())
