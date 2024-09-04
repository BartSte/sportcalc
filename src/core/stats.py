from dataclasses import dataclass
from datetime import time


@dataclass
class ExerciseStats:
    """
    Based on the attributes, a set of cycling statistics are calculated and
    presented as properties.

    The "conventional racing bike parameters" of the following study were used:
        - https://www.sheldonbrown.com/rinard/aero/formulas.html

    Attributes
    ----------
        air_density_kgpm3: float
            Air density in kg/m^3.
        distance_m: float
            Distance cycled in meters.
        gravity: float
            Gravity in m/s^2.
        time: time
            Time taken to cycle the distance in seconds.
        weight_kg: float
            Weight of the cyclist + bike in kg.

    """

    distance_m: float
    time: time
    weight_kg: float

    air_density_kgpm3: float = 1.293
    gravity: float = 9.81

    def as_dict(self, exclude: tuple[str, ...] = tuple()) -> dict:
        """
        Return the inputs, results, and constants as a dictionary.

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
    def speed_ms(self) -> float:
        """
        The average speed in m/s.

        Returns
        -------
            the average speed in m/s

        """
        return self.distance_m / self.time_s

    @property
    def speed_kmph(self) -> float:
        """
        Return the average speed in km/h.

        Returns
        -------
            the average speed in km/h

        """
        return self.speed_ms * 3.6
