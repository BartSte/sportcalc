from argparse import Action, ArgumentParser, Namespace, RawTextHelpFormatter
from importlib.metadata import entry_points
from typing import Any

from sportcalc._core.cli.type_parsers import parse_time
from sportcalc._core.stats import ExerciseStats


class CoreParser(ArgumentParser):
    """Parser for the core module."""

    distance_km: Action

    def __init__(self, *args: Any, **kwargs: Any):
        """Create a new CoreParser."""
        super().__init__(*args, **kwargs)

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
        """Parse the arguments."""
        parsed_args: Namespace = super().parse_args(*args, **kwargs)
        parsed_args.distance_m = parsed_args.distance_km * 1000

        return parsed_args


def make_top_level_parser() -> ArgumentParser:
    """Create the top level parser.

    This parser merely instructs the user to use one of the console-scripts
    instead.

    Returns
        The top level parser.
    """
    sports = _list_supported_sports()
    bullet_list = "\n".join(f"  • {sport}" for sport in sports)
    description = (
        "Calculator the energy consumption for various sports.\n\n"
        "Please use one of the following command line commands for a specific "
        f"sport:\n{bullet_list}\n\nRun `<command> --help' for more "
        "details on a specific sport."
    )
    return ArgumentParser(
        prog="sportcalc",
        description=description,
        formatter_class=RawTextHelpFormatter,
    )


def _list_supported_sports() -> list[str]:
    """Return console-script names that launch sport calculators.

    Returns
        The list of sport calculator names.
    """
    command = entry_points(group="console_scripts")
    return sorted(x.name for x in command if x.value.startswith("sportcalc."))
