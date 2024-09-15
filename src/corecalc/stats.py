import json
from datetime import datetime
from os.path import join
from typing import Any

from corecalc import paths
from corecalc.conversions import datetime2seconds, ms2kmh


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
    time: datetime
    weight_kg: float
    speed_ms: float
    speed_kmph: float

    AIR_DENSITY_KGPM3: float = 1.293
    GRAVITY_N: float = 9.81

    def __init__(
        self, distance_m: float, time: datetime, weight_kg: float, **_
    ):
        """
        Constructor.

        Args:
            distance_m: the distance traveled in meters
            time: the time taken to travel the distance
            weight_kg: the weight of the human + equipment in kg

        """
        self.distance_m: float = distance_m
        self.time: datetime = time
        self.weight_kg: float = weight_kg

    def update(self) -> None:
        """
        Set the values of attributes that are not represented by a property.

        For distingushing between the two, the following convention is used:
            - attributes set by the contructor that are represented by a different
              unit (m vs km) are repeated by a property.
            - value that are a result of the constructor arguments are calculated
              in a function whose output is to an attribute within the `update`
              method.

        """
        self.speed_ms = self.distance_m / self.time_s
        self.speed_kmph = ms2kmh(self.speed_ms)

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

    def summarize(self) -> str:
        """
        Return the string representation of the object.

        Returns
        -------
            the string representation of the object

        """
        inputs: str = join(paths.static, "inputs.template")
        with open(inputs) as inputs_file:
            return inputs_file.read().format(**self.as_dict())

    def json(self, indent: int = 4, **kwargs) -> str:
        """
        Return the object as a JSON string.

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
        """
        Return the time taken to cycle the distance in seconds.

        Returns
        -------
            the time taken to cycle the distance in seconds

        """
        return datetime2seconds(self.time)

    @property
    def time_h(self) -> float:
        """
        Return the time taken to cycle the distance in hours.

        Returns
        -------
            the time taken to cycle the distance in hours

        """
        return self.time_s / 3600

    @property
    def distance_km(self) -> float:
        """
        Return the distance cycled in kilometers.

        Returns
        -------
            the distance cycled in kilometers

        """
        return self.distance_m / 1000
