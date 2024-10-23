from corecalc.cli.parser import CoreParser


class SpeedSkatingParser(CoreParser):
    """
    Parser for SpeedSkatingStats.

    Adds support for the unit `laps` to the distance argument.

    Attributes:
        lap_distance_km: the distance of one lap in km.

    """

    lap_distance_km: float

    def __init__(self, *args, lap_distance_km: float = 0.4, **kwargs):
        """
        Constructor.

        Args:
            lap_distance_km: the distance of one lap in km.
            *args: passed to the CoreParser.
            **kwargs: passed to the CoreParser.
        """
        super().__init__(*args, **kwargs)
        self.lap_distance_km = lap_distance_km

        self.distance_km.type = self._parse_distance
        self.distance_km.help = (
            "Distance skated in km. When the number is appended by `laps` "
            "the number is multiplied by `lap_distance_km` km. For example,"
            " 10 laps equals 4 km for a `lap_distance_km` of 0.4 km."
        )

    def _parse_distance(self, distance: str) -> float:
        """
        Return the distance in km.

        When the distance is appended by `laps` the number is multiplied by 0.4
        km.

        Args:
            distance: The distance in km or laps.

        Returns:
            the distance in km.

        """
        distance = distance.lower()
        if distance.endswith(("l", "lap", "laps")):
            return float(distance.rstrip("laps")) * self.lap_distance_km
        return float(distance)
