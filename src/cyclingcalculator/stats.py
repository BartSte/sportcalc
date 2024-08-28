import json
from dataclasses import dataclass
from datetime import time


@dataclass
class CyclingStats:
    """
    Based on the attributes, a set of cycling statistics are calculated and
    presented as properties.

    The "conventional racing bike parameters" of the following study were used:
        - https://www.sheldonbrown.com/rinard/aero/formulas.html

    Attributes
    ----------
        air_density_kgpm3: float
            Air density in kg/m^3.
        ascend_m: float
            Total ascent in meters.
        descent_m: float
            Total descent in meters.
        distance_m: float
            Distance cycled in meters.
        drag_coefficient_times_area_m2: float
            Drag coefficient times the frontal area in m^2.
        drive_train_efficiency: float
            Drive train efficiency.
        gravity: float
            Gravity in m/s^2.
        human_efficiency: float
            Human efficiency.
        roll_resistance: float
            Coefficient of rolling resistance.
        time: time
            Time taken to cycle the distance in seconds.
        weight_kg: float
            Weight of the cyclist + bike in kg.

    """

    ascend_m: float
    descent_m: float
    distance_m: float
    time: time
    weight_kg: float

    air_density_kgpm3: float = 1.293
    drag_coefficient_times_area_m2: float = 0.39
    efficiency_drive_train: float = 0.98
    efficiency_human: float = 0.25
    gravity: float = 9.81
    roll_resistance: float = 0.003

    _INPUTS: str = """
--------------------------------------------------------------------------------
INPUTS
--------------------------------------------------------------------------------
Time:               {time}
Weight:             {weight_kg:.2f} kg
Distance:           {distance_km:.2f} km
Average speed:      {speed_kmph:.2f} km/h
"""

    _RESULTS: str = """
--------------------------------------------------------------------------------
RESULTS
--------------------------------------------------------------------------------
Energy consumption human:
    - Drag:                 {energy_drag_kj:>5.0f} kJ
    - Gravity:              {energy_gravity_kj:>5.0f} kJ
    - Rolling resistance:   {energy_roll_kj:>5.0f} kJ
    - Total:                {energy_kj:>5.0f} kJ / {energy_kcal:.0f} kcal
Average power on the pedals:
    - Drag:                 {avg_power_drag_w:>5.0f} W
    - Gravity:              {avg_power_gravity_w:>5.0f} W
    - Rolling resistance:   {avg_power_roll_w:>5.0f} W
    - Total:                {avg_power_w:>5.0f} W
"""

    @property
    def summary(self) -> str:
        """
        Return the inputs and results as a string.

        Returns
        -------
            the inputs and results as a string

        """
        kwargs: dict = self.as_dict()
        return self._INPUTS.format(**kwargs) + self._RESULTS.format(**kwargs)

    def as_dict(self, exclude: list["str"] | None = None) -> dict:
        """
        Return the inputs, results, and constants as a dictionary.

        Returns
        -------
            the inputs, results, and constants as a dictionary

        """
        exclude = exclude or []
        exclude = ["summary", "detailed", "json", "as_dict", *exclude]
        kwargs: dict = {
            k: getattr(self, k)
            for k in dir(self)
            if not k.startswith("_") and k not in exclude
        }
        return kwargs

    @property
    def json(self) -> str:
        """
        Return the result as a JSON string.

        Returns
        -------
            the result as a JSON string

        """
        non_si_units: tuple[str, ...] = "kj", "kmph", "km"
        exclude: list[str] = [x for x in dir(self) if x.endswith(non_si_units)]
        exclude.append("time")
        result: dict = self.as_dict(exclude)
        return json.dumps(result, indent=2)

    @property
    def time_s(self) -> float:
        """
        Return the time taken to cycle the distance in seconds.

        Returns
        -------
            the time taken to cycle the distance in seconds

        """
        return self.time.hour * 3600 + self.time.minute * 60 + self.time.second

    @property
    def distance_km(self) -> float:
        """
        Return the distance cycled in kilometers.

        Returns
        -------
            the distance cycled in kilometers

        """
        return self.distance_m / 1000

    @property
    def speed_kmph(self) -> float:
        """
        Return the average speed in km/h.

        Returns
        -------
            the average speed in km/h

        """
        return self.distance_km / (self.time_s / 3600)

    @property
    def speed_ms(self) -> float:
        """
        The average speed in m/s.

        Returns
        -------
            the average speed in m/s

        """
        return self.distance_m / self.time_s

    @property
    def work_j(self) -> float:
        """
        Return the work done in joules without any efficiency losses.

        Returns
        -------
            the work that is done in joules

        """
        return self._calc_work()

    def _calc_work(self, efficiency: float = 1.0) -> float:
        """
        Return the work done in joules using the given `efficiency`.

        3 forces are considered that the cyclist has to overcome:
            - Rolling resistance, created by the tires on the road.
            - Drag, created by the air resistance.
            - Gravity, created by the slope of the road.

        Using these forces, and the traveled distance, the work that needs to be
        done in joules is calculated.

        In reality, the cyclist and the drive train are not 100% efficient.
        Hence, the work done by the human will be greater than the energy that
        is actually supplied to the pedals. This is taken into account by the
        `efficiency_human` and the `efficiency_drive_train` parameters.

        In the case of a cyclist, the efficiency is typically around 0.25. Thus,
        the work supplied by the cyclist must be divided by the efficiency to
        get the actual energy needed by the cyclist.

        In the case of the drive train, the efficiency is typically around 0.95.
        This means that 5% of the energy supplied by the cyclist to the pedals
        is lost in the drive train.

        The human and drive train efficiency are combined in the `efficiency`
        parameter that is applied to the `work_drag_j`, `work_gravity_j`, and
        `work_roll_j` properties.
        return self.work_drag_j + self.work_gravity_j + self.work_roll_j

        Arguments:
        ---------
            efficiency: the efficiency of the human and drive train

        Returns:
        -------
            the work done in joules

        """
        work_j = self.work_drag_j + self.work_ascend_j + self.work_roll_j
        return (work_j / efficiency) + self.work_descend_j

    @property
    def work_drag_j(self) -> float:
        """
        Return the work done to overcome the drag in joules.

        Note that no efficiency is applied here.

        Returns
        -------
            the work done to overcome the drag in joules

        """
        return self.distance_m * self.force_drag

    @property
    def force_drag(self) -> float:
        """
        The drag is calculated by using the drag coefficient times the frontal
        area.


        Returns
        -------
            the drag in N

        """
        return (
            0.5
            * self.drag_coefficient_times_area_m2
            * self.air_density_kgpm3
            * self.speed_ms**2
        )

    @property
    def work_ascend_j(self) -> float:
        """
        Return the work done to ascend in joules.

        Note that no efficiency is applied here.

        Returns
        -------
            the work done to ascend in joules

        """
        return self.ascend_m * self.force_gravity

    @property
    def work_descend_j(self) -> float:
        """
        Return the work done to descend in joules.

        This work is always negative, since the cyclist is descending.

        Returns
        -------
            the work done to descend in joules

        """
        return -self.descent_m * self.force_gravity

    @property
    def force_gravity(self) -> float:
        """
        The work done to overcome the gravity is calculated detemined the
        potential energy difference between the start and end of the ride.


        Returns
        -------
            the gravity in N

        """
        return self.weight_kg * self.gravity

    @property
    def work_roll_j(self) -> float:
        """
        Return the work done to overcome the rolling resistance in joules.

        Note that no efficiency is applied here.

        Returns
        -------
            the work done to overcome the rolling resistance in joules

        """
        return self.distance_m * self.force_roll

    @property
    def force_roll(self) -> float:
        """
        The rolling resistance is calculated by the weight of the cyclist and
        bike times the coefficient of rolling resistance.

        Returns
        -------
            the rolling resistance in N

        """
        return self.force_gravity * self.roll_resistance

    @property
    def energy_j(self) -> float:
        """
        Return the energy consumption of the cyclist in kilojoules.

        Returns
        -------
            the energy consumption of the cyclist in kilojoules

        """
        return self._calc_work(self.efficiency)

    @property
    def efficiency(self) -> float:
        """
        Return the efficiency of the cyclist and drive train.

        Returns
        -------
            the efficiency of the cyclist and drive train

        """
        return self.efficiency_human * self.efficiency_drive_train

    @property
    def energy_kj(self) -> float:
        """
        Return the energy consumption of the cyclist in kilojoules.

        Returns
        -------
            the energy consumption of the cyclist in kilojoules

        """
        return j2kj(self.energy_j)

    @property
    def energy_kcal(self) -> float:
        """
        Return the energy consumption of the cyclist in kcal.

        Returns
        -------
            the energy consumption of the cyclist in kcal

        """
        return j2kcal(self.energy_j)

    @property
    def energy_drag_j(self) -> float:
        """
        Return the energy consumption to overcome the drag in joules.

        Returns
        -------
            the energy consumption to overcome the drag in joules

        """
        return self.work_drag_j / self.efficiency

    @property
    def energy_drag_kj(self) -> float:
        """
        Return the energy consumption to overcome the drag in kilojoules.

        Returns
        -------
            the energy consumption to overcome the drag in kilojoules

        """
        return j2kj(self.energy_drag_j)

    @property
    def energy_roll_j(self) -> float:
        """
        Return the energy consumption to overcome the rolling resistance in
        joules.

        Returns
        -------
            the energy consumption to overcome the rolling resistance in joules

        """
        return self.work_roll_j / self.efficiency

    @property
    def energy_roll_kj(self) -> float:
        """
        Return the energy consumption to overcome the rolling resistance in
        kilojoules.

        Returns
        -------
            the energy consumption to overcome the rolling resistance in
            kilojoules

        """
        return j2kj(self.energy_roll_j)

    @property
    def energy_gravity_j(self) -> float:
        """
        Return the energy consumption to overcome the gravity in joules.

        Returns
        -------
            the energy consumption to overcome the gravity in joules

        """
        return self.work_ascend_j / self.efficiency

    @property
    def energy_gravity_kj(self) -> float:
        """
        Return the energy consumption to overcome the gravity in kilojoules.

        Returns
        -------
            the energy consumption to overcome the gravity in kilojoules

        """
        return j2kj(self.energy_gravity_j)

    @property
    def avg_power_w(self) -> float:
        """
        Return the average power that is applied to the pedals in watt.

        Note that we only need to consider the drive train efficiency here,
        since we are interested in the power that is applied to the pedals, not
        by the human itself.

        Returns
        -------
            the average power output in watt

        """
        return self._calc_work(self.efficiency_drive_train) / self.time_s

    @property
    def avg_power_drag_w(self) -> float:
        """
        Return the average power that is applied to the pedals to overcome the
        drag in watt.

        Returns
        -------
            the average power to overcome the drag in watt

        """
        return (self.work_drag_j / self.efficiency_drive_train) / self.time_s

    @property
    def avg_power_gravity_w(self) -> float:
        """
        Return the average power that is applied to the pedals to overcome the
        gravity in watt.

        Returns
        -------
            the average power to overcome the gravity in watt

        """
        work_gravity_j = (
            self.work_ascend_j / self.efficiency_drive_train
        ) + self.work_descend_j

        return work_gravity_j / self.time_s

    @property
    def avg_power_roll_w(self) -> float:
        """
        Return the average power that is applied to the pedals to overcome the
        rolling resistance in watt.

        Returns
        -------
            the average power to overcome the rolling resistance in watt

        """
        return (self.work_roll_j / self.efficiency_drive_train) / self.time_s


def j2kj(joules: float) -> float:
    """
    Return the energy in Joules as kilojoules.

    Arguments:
    ---------
        joules: the energy in Joules

    Returns:
    -------
        the energy in kilojoules

    """
    return joules / 1000


def j2kcal(joules: float) -> float:
    """
    Return the energy in Joules as kcal.

    Arguments:
    ---------
        joules: the energy in Joules

    Returns:
    -------
        the energy in kcal

    """
    return joules / 4184
