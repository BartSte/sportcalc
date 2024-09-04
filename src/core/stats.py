from dataclasses import dataclass
from datetime import time
import json
from os.path import join
from typing import Any

from core import paths


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

    @classmethod
    def from_dict(cls, data: dict) -> "ExerciseStats":
        """
        Create a new ExerciseStats from a dictionary.

        This is different from just expanding the dictionary (i.e., `**data`)
        as this approach allows for the dictionary to have additional keys
        without throwing an error.

        Returns
        -------
            a new ExerciseStats from a dictionary

        """
        kwargs: dict = {
            key: data[key]
            for key in cls.__dataclass_fields__.keys()
            if key in data
        }
        return cls(**kwargs)
