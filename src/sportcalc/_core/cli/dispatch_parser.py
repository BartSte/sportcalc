from argparse import Action, ArgumentParser, Namespace
from collections.abc import Callable
from typing import Any

from sportcalc import cycling, running, speedskating, walking

MainFunction = Callable[[list[str] | None], str]


class DispatchParser(ArgumentParser):
    """Parser that selects a sport and binds its main() as the handler."""

    def __init__(self, *args, **kwargs: Any) -> None:
        """Init.

        Args:
            **kwargs: Keyword arguments passed to ArgumentParser. 'add_help' is forced to False.
        """
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)

        self.add_argument(
            "sport",
            choices=list(FuncSetter.functions),
            nargs="?",
            action=FuncSetter,
            help="The name of the sport to calculate the energy consumption for.",
        )
        self.add_argument(
            "-h", "--help", action="store_true", help="Show help message"
        )


class FuncSetter(Action):
    """argparse action that stores the sport and its entry function in the namespace."""

    functions: dict[str, MainFunction] = {
        "cycling": cycling.main,
        "running": running.main,
        "speedskating": speedskating.main,
        "walking": walking.main,
    }

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str | None,
        option_string: str | None = None,
    ) -> None:
        """Set selected sport and bind its entry function.

        Args:
            parser: The active ArgumentParser.
            namespace: Namespace to populate (adds 'sport' and 'func').
            value: The chosen sport name.
            option_string: The triggering option string, if any.
        """
        namespace.sport = value
        namespace.func = self.functions.get(value)
