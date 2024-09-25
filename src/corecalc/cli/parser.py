from argparse import ArgumentParser

from corecalc.cli.type_parsers import parse_time
from corecalc.stats import ExerciseStats


class ExerciseParser(ArgumentParser):
    """Parser for the core module."""

    def __init__(self, *args, **kwargs):
        """Create a new CoreParser."""
        super().__init__(*args, **kwargs)

        self.add_argument(
            "weight_kg",
            action="store",
            type=float,
            help="Weight of the cyclist + bike in kg.",
        )

        self.add_argument(
            "distance_km",
            action="store",
            type=float,
            help="Distance cycled in km.",
        )

        self.add_argument(
            "time",
            action="store",
            type=parse_time,
            help="The elapsed time as an iso format string (HH:MM:SS) or as a "
            "float representing the number of hours.",
        )

        self.add_argument(
            "ascent_m",
            action="store",
            type=float,
            default=ExerciseStats.ascent_m,
            nargs="?",
            help="Total ascent in meters (default: 0).",
        )

        self.add_argument(
            "descent_m",
            action="store",
            type=float,
            default=ExerciseStats.descent_m,
            nargs="?",
            help="Total descent in meters (default: 0).",
        )

        self.add_argument(
            "-a",
            "--air-density-kgpm3",
            action="store",
            default=ExerciseStats.air_density_kgpm3,
            type=float,
            help="Air density in kg/m^3 (default: 1.293 km/m^3).",
        )

        self.add_argument(
            "-j",
            "--json",
            action="store_true",
            help="Send the output as a JSON string to stdout.",
        )

        self.add_argument(
            "-l",
            "--loglevel",
            action="store",
            default="WARNING",
            help="Set the log level.",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        )

    def parse_args(self, *args, **kwargs):
        """Parse the arguments."""
        args = super().parse_args(*args, **kwargs)
        args.distance_m = args.distance_km * 1000

        return args
