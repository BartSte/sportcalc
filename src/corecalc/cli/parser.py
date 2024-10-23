import logging
from argparse import Action, ArgumentParser
from contextlib import suppress

from corecalc.cli.type_parsers import parse_time
from corecalc.stats import ExerciseStats


class CoreParser(ArgumentParser):
    """Parser for the core module."""

    def __init__(self, *args, **kwargs):
        """Create a new CoreParser."""
        super().__init__(*args, **kwargs)

        self.add_argument(
            "weight_kg",
            action="store",
            type=float,
            help="Total mass in kg",
        )

        self.add_argument(
            "distance_km",
            action="store",
            type=float,
            help="Distance travelled in km.",
        )

        self.add_argument(
            "time",
            action="store",
            type=parse_time,
            help=(
                "The elapsed time. It can be provided in iso format (HH:MM:SS)"
                "or as a float followed by a time unit (s/sec/seconds, "
                "m/min/minutes, h/hr/hour/hours). A single float is interpreted"
                "as hours."
            ),
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
            help="Total descent in meters (default: ascent value).",
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

    def add_argument(self, *args, **kwargs) -> Action:
        """
        Add an argument to the parser.

        The argument is removed first if it is already present in the parser.

        Args:
            *args: The positional arguments passed to the ArgumentParser.
            **kwargs: The keyword arguments passed to the ArgumentParser.

        """
        self.remove_argument(args[0])
        return super().add_argument(*args, **kwargs)

    def remove_argument(self, name):
        """
        Remove an argument from the parser.

        Args:
            name: The name of the argument to remove.

        """
        with suppress(StopIteration):
            duplicate: Action = next(x for x in self._actions if name == x.dest)
            self._remove_action(duplicate)
            logging.debug(f"Removed argument: {name}")

    def parse_args(self, *args, **kwargs):
        """Parse the arguments."""
        args = super().parse_args(*args, **kwargs)
        args.distance_m = args.distance_km * 1000

        return args
