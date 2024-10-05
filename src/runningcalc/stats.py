from corecalc.stats import MetsSpeedStats


class RunningStats(MetsSpeedStats):
    """
    Statistics for a running exercise.

    The MET values per speed were obtained from the following document:

        - https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pd

    I comapered the results with the following calculator:

        - TODO
    """

    METS_KM_H: tuple[float, ...] =      (8.0,  9.6, 10.7, 12.0, 13.8, 16.1)
    METS_KCAL_KG_H: tuple[float, ...] = (8.0, 10.0, 11.0, 12.5, 14.0, 16.0)
