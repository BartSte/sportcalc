import json
import logging
from datetime import datetime
from typing import Any

import numpy as np

from sportcalc._core import static
from sportcalc._core.conversions import datetime2seconds, kcal2j, ms2kmh


class ExerciseStats:
    """Based on the attributes, a set of statistics are calculated when the `update`
    method is called. The results can be summarized as a string or as a JSON
    string.

    Attributes
    ----------
        air_density_kgpm3: float
            Air density in kg/m^3.
        distance_m: float
            Distance travelled in meters.
        gravity: float
            Gravity in m/s^2.
        time: time
            Elapsed time in seconds.
        weight_kg: float
            Weight of the human + equipment in kg.

    """

    distance_m: float
    time: datetime
    weight_kg: float
    speed_ms: float
    speed_kmph: float
    ascent_m: float = 0
    descent_m: float = 0
    air_density_kgpm3: float = 1.293

    GRAVITY_N: float = 9.81

    def __init__(
        self,
        *,
        distance_m: float,
        time: datetime,
        weight_kg: float,
        ascent_m: float,
        descent_m: float,
        air_density_kgpm3: float,
        **_,
    ) -> None:
        """Initialize.

        Args:
            distance_m: the distance traveled in meters
            time: the time taken to travel the distance
            weight_kg: the weight of the human + equipment in kg
            ascent_m: the total ascent in meters
            descent_m: the total descent in meters
            air_density_kgpm3: the air density in kg/m^3 (default: 1.293)

        """
        self.distance_m = distance_m
        self.time = time
        self.weight_kg = weight_kg
        self.ascent_m = ascent_m
        self.descent_m = descent_m
        self.air_density_kgpm3 = air_density_kgpm3

    def update(self) -> None:
        """Set the values of attributes that are not represented by a property.

        For distingushing between the two, the following convention is used:
            - attributes set by the contructor that are represented by a different
              unit (m vs km) are repeated by a property.
            - value that are a result of the constructor arguments are calculated
              in a function whose output is to an attribute within the `update`
              method.

        """
        self.speed_ms = self.distance_m / self.time_s
        self.speed_kmph = ms2kmh(self.speed_ms)

    def as_dict(self, exclude: tuple[str, ...] = ()) -> dict:
        """Return the inputs, results, and constants as a dictionary.

        Returns
        -------
            the inputs, results, and constants as a dictionary

        """
        kwargs: dict = {
            key: getattr(self, key)
            for key in dir(self)
            if key not in exclude
            and not key.startswith("_")
            and not callable(getattr(self, key))
        }

        return kwargs

    def summarize(self) -> str:
        """Return the string representation of the object.

        Returns
        -------
            the string representation of the object

        """
        inputs: str = static.join("inputs.template")
        with open(inputs) as inputs_file:
            return inputs_file.read().format(**self.as_dict())

    def json(self, indent: int = 4, **kwargs: Any) -> str:
        """Return the object as a JSON string.

        Returns
        -------
            the object as a JSON string

        """
        # TODO exclude non-SI from json
        # non_si_units: tuple[str, ...] = "kj", "kmph", "km"
        # exclude_non_si = [x for x in dir(self) if x.endswith(non_si_units)]
        # exclude.extend(exclude_non_si)
        # TODO make a serializer for time
        as_dict: dict[str, Any] = self.as_dict()
        as_dict["time"] = as_dict["time"].strftime("%H:%M:%S")
        return json.dumps(as_dict, indent=indent, **kwargs)

    @property
    def time_s(self) -> float:
        """Return the time taken to travel the distance in seconds.

        Returns
        -------
            the time taken to travel the distance in seconds

        """
        return datetime2seconds(self.time, check=True)

    @property
    def time_h(self) -> float:
        """Return the time taken to travel the distance in hours.

        Returns
        -------
            the time taken to travel the distance in hours

        """
        return self.time_s / 3600

    @property
    def distance_km(self) -> float:
        """Return the distance traveled in kilometers.

        Returns
        -------
            the distance traveled in kilometers

        """
        return self.distance_m / 1000


class MetsStats(ExerciseStats):
    """Use the METs value for a specific exercise to calculate the energy
    consumption.
    """

    mets_kcal_kg_h: float
    energy_kcal: float
    energy_kj: float

    def summarize(self) -> str:
        """Return a string containing a summary of the statistics.

        Returns
        -------
            a string containing a summary of the statistics

        """
        template: str = static.join("results_mets.template")
        with open(template) as results_file:
            txt: str = results_file.read().format(**self.as_dict())
            return super().summarize() + txt

    def update(self) -> None:
        """Override the parent method to include the calculation of the energy
        consumption.
        """
        super().update()
        self.energy_kcal = self.calc_energy_kcal(self.mets_kcal_kg_h)
        self.energy_kj = kcal2j(self.energy_kcal) * 1e-3

    def calc_energy_kcal(self, mets_kcal_kg_h: float) -> float:
        """Return the work done in joules.

        1 is subtracted from the MET value to ensure that we ulate the
        active energy expenditure only. Otherwise, the resting energy
        expenditure would be included.

        Arguments:
        ---------
            mets_kcal_kg_h : float
                the metabolic equivalent of task (kcal/km/kg

        Returns:
        -------
            the work done in joules

        """
        mets_active_only: float = mets_kcal_kg_h - 1
        return mets_active_only * self.weight_kg * self.time_h


class MetsSpeedStats(MetsStats):
    """Similar to `MetsBasedStats` but now the METs value depends on the speed.

    The values can be provided as two tuples: one for the speed in km/h and the
    other for the METs value in kcal/km/kg. Missing values are interpolated.

    Attributes
    ----------
        METS_KM_H: tuple[float, ...]
            The speed in km/h at which the METs value was measured.
        METS_KCAL_KG_H: tuple[float, ...]
            The METs value in kcal/km/kg at the corresponding speed.

    """

    METS_KM_H: tuple[float, ...]
    METS_KCAL_KG_H: tuple[float, ...]

    def update(self) -> None:
        """Override the parent method.

        Include the calculation of the energy consumption using the METs value
        that is dependent on the speed.
        """
        ExerciseStats.update(self)
        self.mets_kcal_kg_h = self.calc_mets_kcal_kg_h(self.speed_kmph)
        self.energy_kcal = self.calc_energy_kcal(self.mets_kcal_kg_h)
        self.energy_kj = kcal2j(self.energy_kcal) * 1e-3

    def calc_mets_kcal_kg_h(self, speed_kmph: float) -> float:
        """Return the metabolic equivalent of task.

        This is done by converting the MET value to kcal/km/kg.

        Arguments:
        ---------
            speed_kmph : float
                the speed in km/h

        Returns:
        -------
            the metabolic equivalent of task (kcal/km/kg)

        """
        is_out_of_range: bool = (
            speed_kmph < self.METS_KM_H[0] or speed_kmph > self.METS_KM_H[-1]
        )
        if is_out_of_range:
            logging.warning(
                f"The speed {speed_kmph} km/h is out of the range data was"
                f" collected for. Values outside {self.METS_KM_H[0]} - "
                f"{self.METS_KM_H[-1]} km/h may not be accurate."
            )

        mets: np.ndarray = np.interp(
            speed_kmph, self.METS_KM_H, self.METS_KCAL_KG_H
        )
        return float(mets)
