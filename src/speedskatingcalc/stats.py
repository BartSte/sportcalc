from corecalc.stats import MetsSpeedStats


class SpeedSkatingStats(MetsSpeedStats):
    """
    Statistics for a walking exercise.

    - source:
        https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pdf
        https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pdf
    """

    METS_KCAL_KG_H = 5.0, 6.0, 7.0, 9.0, 13.3
    METS_KM_H = 10, 15, 20, 30, 35
