import logging
from dataclasses import dataclass
from os.path import join

import numpy as np
from core.stats import ExerciseStats
from numpy._core.multiarray import ndarray

from running import paths


@dataclass
class RunningStats(ExerciseStats):
    """
    The MET values per speed were obtained from the following document:

        - https://media.hypersites.com/clients/1235/filemanager/MHC/METs.pd

    I comapered the results with the following calculator:

        -
    """

    METS_KM_H: tuple[float, ...] = (8.0, 9.6, 10.7, 12.0, 13.8, 16.1)
    METS_KCAL_KG_H: tuple[float, ...] = (8.0, 10.0, 11.0, 12.5, 14.0, 16.0)

    def summarize(self) -> str:
        """
        Return a string containing a summary of the cycling statistics.

        Returns
        -------
            a string containing a summary of the cycling statistics

        """
        template: str = join(paths.static, "results.template")
        with open(template) as results_file:
            txt: str = results_file.read().format(**self.as_dict())
            return super().summarize() + txt

    @property
    def energy_kj(self) -> float:
        """
        Return the work done in kilojoules.

        Returns
        -------
            the work done in kilojoules

        """
        return self.energy_kcal * 4.184

    @property
    def energy_kcal(self) -> float:
        """
        Return the work done in joules.

        1 is subtracted from the MET value to ensure that we calculate the
        active energy expenditure only. Otherwise, the resting energy
        expenditure would be included.

        Returns
        -------
            the work done in joules

        """
        mets_active_only: float = self.mets_kcal_kg_h - 1
        return mets_active_only  * self.weight_kg * self.time_h

    @property
    def mets_kcal_kg_h(self) -> float:
        """
        Return the metabolic equivalent of task.

        This is done by converting the MET value to kcal/km/kg.

        Returns
        -------
            the metabolic equivalent of task (kcal/km/kg)

        """
        is_out_of_range: bool = (
            self.speed_kmph < self.METS_KM_H[0]
            or self.speed_kmph > self.METS_KM_H[-1]
        )
        if is_out_of_range:
            logging.warning(
                f"The speed {self.speed_kmph} km/h is out of the range data was"
                f" collected for. Values outside {self.METS_KM_H[0]}-"
                f"{self.METS_KM_H[-1]} km/h may not be accurate."
            )

        mets: ndarray = np.interp(
            self.speed_kmph, self.METS_KM_H, self.METS_KCAL_KG_H
        )
        return float(mets)
