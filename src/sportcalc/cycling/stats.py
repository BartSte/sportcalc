from typing import override

from sportcalc._core.conversions import j2kcal, j2kj
from sportcalc._core.stats import ExerciseStats
from sportcalc.cycling import static


class CyclingStats(ExerciseStats):
    """A set of cycling statistics are calculated and presented as properties.

    The "conventional racing bike parameters" of the following study were used:
        - https://www.sheldonbrown.com/rinard/aero/formulas.html

    Constants
    ---------
        DRAG_COEFFICIENT_TIMES_AREA_M2: float
            Drag coefficient times the frontal area in m^2.
        DRAFT_FACTOR: float
            The fraction by which the drag is reduced when drafting behind
            another cyclist.
        DRIVE_TRAIN_EFFICIENCY: float
            Drive train efficiency.
        HUMAN_EFFICIENCY: float
            Human efficiency.
        ROLL_RESISTANCE: float
            Coefficient of rolling resistance.
        EFFICIENCY: float
            The efficiency of the human and drive train combined.

    Attributes constructor
    ----------------------
        ascent_m: float
            Total ascent in meters.
        descent_m: float
            Total descent in meters.
        fraction_spend_drafting: float
            The fraction of time spent drafting behind another cyclist. Default
            is 0, meaning no drafting. A value of 1.0 means you spent all your
            time drafting.

    Attributes draft
    ----------------
        avg_draft_factor: float
            A unitless number that represents the reduction in drag due to
            drafting behind another cyclist.
        force_drag: float
            The force needed to overcome the drag in N.
        work_drag_j: float
            The work done to overcome the drag in joules.
        energy_drag_j: float
            The energy needed to overcome the drag in joules.
        energy_drag_kj: float
            The energy needed to overcome the drag in kilojoules.
        avg_power_drag_w: float
            The average power delivered to the pedals by the cyclist to overcome
            the drag.

    Attributes gravity
    ------------------
        force_gravity: float
            The gravitational force in N.
        work_ascent_j: float
            The work done during the ascent in joules.
        work_descend_j: float
            The work done during the descent in joules.
        energy_gravity_j: float
            The energy needed to overcome the gravity in joules.
        energy_gravity_kj: float
            The energy needed to overcome the gravity in kilojoules.
        avg_power_gravity_w: float
            The average power delivered to the pedals by the cyclist to overcome
            the gravity.

    Attributes roll
    ---------------
        force_roll: float
            The force needed to overcome the rolling resistance in N.
        work_roll_j: float
            The work done to overcome the rolling resistance in joules.
        energy_roll_j: float
            The energy needed to overcome the rolling resistance in joules.
        energy_roll_kj: float
            The energy needed to overcome the rolling resistance in kilojoules.
        avg_power_roll_w: float
            The average power delivered to the pedals by the cyclist to overcome
            the rolling resistance.

    Attributes energy consumption
    -----------------------------
        work_j: float
            The work done in joules.
        energy_j: float
            The energy consumed by the cyclist in joules.
        energy_kj: float
            The energy consumed by the cyclist in kilojoules.
        energy_kcal: float
            The energy consumed by the cyclist in kilocalories.
        avg_power_w: float
            The average power delivered to the pedals by the cyclist.

    """

    DRAFT_FACTOR: float = 0.3
    DRAG_COEFFICIENT_TIMES_AREA_M2: float = 0.39
    EFFICIENCY_DRIVE_TRAIN: float = 0.98
    EFFICIENCY_HUMAN: float = 0.25
    ROLL_RESISTANCE: float = 0.003
    EFFICIENCY: float = EFFICIENCY_HUMAN * EFFICIENCY_DRIVE_TRAIN

    work_j: float
    fraction_spend_drafting: float = 0

    avg_draft_factor: float
    force_drag: float
    work_drag_j: float
    energy_drag_j: float
    energy_drag_kj: float
    avg_power_drag_w: float

    force_gravity: float
    work_ascent_j: float
    work_descend_j: float
    energy_gravity_j: float
    energy_gravity_kj: float
    avg_power_gravity_w: float

    force_roll: float
    work_roll_j: float
    energy_roll_j: float
    energy_roll_kj: float
    avg_power_roll_w: float

    energy_j: float
    energy_kj: float
    energy_kcal: float
    avg_power_w: float

    def __init__(
        self,
        *,
        fraction_spend_drafting: float = 0,
        **kwargs,
    ):
        """Construct.

        Args:
            fraction_spend_drafting: the fraction of time spent drafting behind
                another cyclist. Default is 0, meaning no drafting. A value of
                1.0 means you spent all your time drafting.
            **kwargs: the keyword arguments passed to the parent class

        """
        super().__init__(**kwargs)
        self.fraction_spend_drafting = fraction_spend_drafting

    def update(self) -> None:
        """Update the statistics that are derived from the constructor arguments."""
        super().update()

        self.avg_draft_factor = self._calc_avg_draft_factor()
        self.force_drag = self._calc_force_drag(self.avg_draft_factor)
        self.work_drag_j = self.distance_m * self.force_drag
        self.energy_drag_j = self.work_drag_j / self.EFFICIENCY
        self.energy_drag_kj = j2kj(self.energy_drag_j)
        self.avg_power_drag_w = self._calc_avg_power_drag_w(self.work_drag_j)

        self.force_gravity = self.weight_kg * self.GRAVITY_N
        self.work_ascent_j = self.ascent_m * self.force_gravity
        self.work_descend_j = -self.descent_m * self.force_gravity
        self.energy_gravity_j = self.work_ascent_j / self.EFFICIENCY
        self.energy_gravity_kj = j2kj(self.energy_gravity_j)
        self.avg_power_gravity_w = self._calc_avg_power_gravity_w(
            self.work_ascent_j, self.work_descend_j
        )

        self.force_roll = self.force_gravity * self.ROLL_RESISTANCE
        self.work_roll_j = self.distance_m * self.force_roll
        self.energy_roll_j = self.work_roll_j / self.EFFICIENCY
        self.energy_roll_kj = j2kj(self.energy_roll_j)
        self.avg_power_roll_w = self._calc_avg_power_roll_w(self.work_roll_j)

        self.work_j = self._calc_work(
            self.work_drag_j,
            self.work_roll_j,
            self.work_ascent_j,
            self.work_descend_j,
        )
        self.energy_j = self._calc_work(
            self.work_drag_j,
            self.work_roll_j,
            self.work_ascent_j,
            self.work_descend_j,
            self.EFFICIENCY,
        )
        self.energy_kj = j2kj(self.energy_j)
        self.energy_kcal = j2kcal(self.energy_j)
        self.avg_power_w = self._calc_avg_power_w(self.work_j)

    @override
    def summarize(self) -> str:
        """Return a string containing a summary of the cycling statistics.

        Returns
        -------
            a string containing a summary of the cycling statistics

        """
        template: str = static.join("results.template")
        with open(template) as results_file:
            txt: str = results_file.read().format(**self.as_dict())
            return super().summarize() + txt

    def _calc_work(
        self,
        work_drag_j: float,
        work_roll_j: float,
        work_ascent_j: float,
        work_descent_j: float,
        efficiency: float = 1.0,
    ) -> float:
        """Return the work done in joules using the given `efficiency`.

        3 forces are considered that the cyclist has to overcome:
            - Rolling resistance, created by the tires on the road.
            - Drag, created by the air resistance.
            - Gravity, created by the slope of the road.

        Using these forces, and the traveled distance, the work that needs to be
        done in joules is calculated.

        In reality, the cyclist and the drive train are not 100% efficient.
        Hence, the work done by the human will be greater than the energy that
        is actually supplied to the pedals. This is taken into account by the
        `efficiency_human` and the `EFFICIENCY_DRIVE_TRAIN` parameters.

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
            work_drag_j: the work done to overcome the drag in joules
            work_roll_j: the work done to overcome the rolling resistance in
            joules
            work_ascent_j: the work done to overcome the ascent in joules
            work_descent_j: the work done to overcome the descent in joules
            efficiency: the efficiency of the human and drive train

        Returns:
        -------
            the work done in joules

        """
        work_j = work_drag_j + work_ascent_j + work_roll_j
        return (work_j / efficiency) + work_descent_j

    def _calc_force_drag(self, avg_draft_factor: float) -> float:
        """Calculate the drag by using the drag coefficient times the frontal area.

        Arguments:
        ---------
            avg_draft_factor: the average draft factor

        Returns:
        -------
            the drag in N

        """
        drafting_reduction: float = 1 - avg_draft_factor
        force: float = (
            0.5
            * self.DRAG_COEFFICIENT_TIMES_AREA_M2
            * self.air_density_kgpm3
            * self.speed_ms**2
        )
        return force * drafting_reduction

    def _calc_avg_draft_factor(self) -> float:
        """Return the average draft factor.

        This factor is determined by the multiplying het `draft_factor` with the
        `time_fraction_spend_drafting`. As a result, the average draft factor
        during the ride is calculated.

        Returns
        -------
            the average draft factor

        """
        return self.DRAFT_FACTOR * self.fraction_spend_drafting

    def _calc_avg_power_w(self, work_j: float) -> float:
        """Return the average power that is applied to the pedals in watt.

        Returns
        -------
            the average power in watt

        """
        return (work_j / self.EFFICIENCY_DRIVE_TRAIN) / self.time_s

    def _calc_avg_power_drag_w(self, work_drag_j: float) -> float:
        """Return the average power that is applied to the pedals to overcome
        the drag in watt.

        Returns
        -------
            the average power to overcome the drag in watt

        """
        return (work_drag_j / self.EFFICIENCY_DRIVE_TRAIN) / self.time_s

    def _calc_avg_power_gravity_w(
        self, work_ascent_j: float, work_descend_j: float
    ) -> float:
        """Return the average power that is applied to the pedals to overcome the
        gravity in watt.

        Returns
        -------
            the average power to overcome the gravity in watt

        """
        work_gravity_j = (
            work_ascent_j / self.EFFICIENCY_DRIVE_TRAIN
        ) + work_descend_j

        return work_gravity_j / self.time_s

    def _calc_avg_power_roll_w(self, work_roll_j: float) -> float:
        """Return the average power that is applied to the pedals to overcome
        the rolling resistance in watt.

        Returns
        -------
            the average power to overcome the rolling resistance in watt

        """
        return (work_roll_j / self.EFFICIENCY_DRIVE_TRAIN) / self.time_s
