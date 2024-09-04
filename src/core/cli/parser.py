from argparse import ArgumentParser

from core.cli.type_parsers import parse_time


class CoreParser(ArgumentParser):
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
            "--json",
            action="store_true",
            help="Send the output as a JSON string to stdout.",
        )

