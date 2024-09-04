from argparse import Namespace
from core.cli.parser import ExerciseParser
from core.cli.type_parsers import parse_percentage


class CyclingParser(ExerciseParser):
    """
    Return the argument parser for the script.

    Returns
    -------
        The argument parser for the script

    """

    _USAGE = (
        "Usage: cycling [options] weight_kg distance_km time ascent_m descent_m"
    )
    _DESCRIPTION = "Calculate the energy consumption while cycling."

    def __init__(
        self,
        prog: str = "cycling",
        usage: str = _USAGE,
        description: str = _DESCRIPTION,
        **kwargs,
    ):
        """
        Create a new CyclingParser.

        Args:
        ----
            prog: the name of the program
            usage: the usage message
            description: the description of the program
            **kwargs: other keyword arguments passed to the CoreParser

        """
        super().__init__(
            prog=prog, usage=usage, description=description, **kwargs
        )

        self.add_argument(
            "ascent_m",
            action="store",
            type=float,
            default=0,
            nargs="?",
            help="Total ascent in meters (default: 0).",
        )

        self.add_argument(
            "descent_m",
            action="store",
            type=float,
            default=0,
            nargs="?",
            help="Total descent in meters (default: 0).",
        )

        self.add_argument(
            "-d",
            "--drafting",
            action="store",
            type=parse_percentage,
            default=0,
            help="Percentage of time spent drafting behind another cyclist. 0 "
            "default, meaning no drafting. A value of 100 means you spent all "
            "your time drafting.",
        )

    def parse_args(self, *args, **kwargs) -> Namespace:
        """
        Parse the arguments.

        Returns
        -------
            The parsed arguments

        """
        args = super().parse_args(*args, **kwargs)
        args.fraction_spend_drafting = args.drafting * 0.01
        return args
