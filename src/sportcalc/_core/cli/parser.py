import sys
from argparse import Action, ArgumentParser, Namespace
from typing import Any

from sportcalc._core.cli.type_parsers import parse_time
from sportcalc._core.stats import ExerciseStats


class SportParser(ArgumentParser):
    """Parser for the core module."""

    _args: list[str]
    distance_km: Action

    def __init__(
        self, *args: Any, argv: list[str] | None = None, **kwargs: Any
    ):
        """Create a new CoreParser.

        Args
            *args: Additional arguments passed to `ArgumentParser`.
            argv: The argv to parse. If not provided, it will use `sys.argv`.
            **kwargs: Additional keyword arguments passed to `ArgumentParser`.

        """
        super().__init__(*args, **kwargs)
        self._args = sys.argv[1:] if argv is None else argv

        self.weight_kg = self.add_argument(
            "weight_kg",
            action="store",
            type=float,
            help="Total mass in kg",
        )

        self.distance_km = self.add_argument(
            "distance_km",
            action="store",
            type=float,
            help="Distance travelled in km.",
        )

        self.time = self.add_argument(
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

        self.ascent_m = self.add_argument(
            "ascent_m",
            action="store",
            type=float,
            default=ExerciseStats.ascent_m,
            nargs="?",
            help="Total ascent in meters (default: 0).",
        )

        self.descent_m = self.add_argument(
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

    def parse_args(self, *args: Any, **kwargs: Any) -> Namespace:
        """Parse arguments and compute derived values.

        Args:
            *args: Positional arguments forwarded to ArgumentParser.parse_args.
            **kwargs: Keyword arguments forwarded to ArgumentParser.parse_args.

        Returns:
            Parsed namespace with an extra 'distance_m' field (meters).
        """
        if not args and "args" not in kwargs:
            kwargs["args"] = self._args
        parsed_args: Namespace = super().parse_args(*args, **kwargs)
        parsed_args.distance_m = parsed_args.distance_km * 1000

        return parsed_args
