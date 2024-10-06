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
        super().__init__(*args, **kwargs)
        self.lap_distance_km = lap_distance_km

        self.add_argument(
            "distance_km",
            action="store",
            type=self._parse_distance,
            help=(
                "Distance skated in km. When the number is appended by `laps` "
                "the number is multiplied by `lap_distance_km` km. For example,"
                " 10 laps equals 4 km for a `lap_distance_km` of 0.4 km."
            ),
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
        if distance.endswith("laps"):
            return float(distance[:-4]) * self.lap_distance_km
        return float(distance)
