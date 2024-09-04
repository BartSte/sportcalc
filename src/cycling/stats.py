from dataclasses import dataclass
from os.path import join

from core.conversions import j2kcal, j2kj
from core.stats import ExerciseStats
from cycling import paths


@dataclass(kw_only=True)
class CyclingStats(ExerciseStats):
    """
    Based on the attributes, a set of cycling statistics are calculated and
    presented as properties.

    The "conventional racing bike parameters" of the following study were used:
        - https://www.sheldonbrown.com/rinard/aero/formulas.html

    Attributes
    ----------
        ascent_m: float
            Total ascent in meters.
        descent_m: float
            Total descent in meters.
        drag_coefficient_times_area_m2: float
            Drag coefficient times the frontal area in m^2.
        draft_factor: float
            The fraction by which the drag is reduced when drafting behind
            another cyclist.
        drive_train_efficiency: float
            Drive train efficiency.
        human_efficiency: float
            Human efficiency.
        roll_resistance: float
            Coefficient of rolling resistance.
        fraction_spend_drafting: float
            The fraction of time spent drafting behind another cyclist. Default
            is 0, meaning no drafting. A value of 1.0 means you spent all your
            time drafting.

    """

    ascent_m: float
    descent_m: float

    draft_factor: float = 0.3
    drag_coefficient_times_area_m2: float = 0.39
    efficiency_drive_train: float = 0.98
    efficiency_human: float = 0.25
    roll_resistance: float = 0.003
    fraction_spend_drafting: float = 0

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
        work_j = self.work_drag_j + self.work_ascent_j + self.work_roll_j
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
        drafting_reduction: float = 1 - self.avg_draft_factor
        force: float = (
            0.5
            * self.drag_coefficient_times_area_m2
            * self.air_density_kgpm3
            * self.speed_ms**2
        )
        return force * drafting_reduction

    @property
    def avg_draft_factor(self) -> float:
        """
        Return the average draft factor.

        This factor is determined by the multiplying het `draft_factor` with the
        `time_fraction_spend_drafting`. As a result, the average draft factor
        during the ride is calculated.

        Returns
        -------
            the average draft factor

        """
        return self.draft_factor * self.fraction_spend_drafting

    @property
    def work_ascent_j(self) -> float:
        """
        Return the work done to ascent in joules.

        Note that no efficiency is applied here.

        Returns
        -------
            the work done to ascent in joules

        """
        return self.ascent_m * self.force_gravity

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
        return self.work_ascent_j / self.efficiency

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
            self.work_ascent_j / self.efficiency_drive_train
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
