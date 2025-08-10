"""Entry point for the sportcalc.speedskating CLI."""

from sportcalc._core import exec
from sportcalc.speedskating.parser import SpeedSkatingParser
from sportcalc.speedskating.stats import SpeedSkatingStats


def main(argv: list[str] | None = None) -> str:
    """Run the speedskating CLI.

    Args:
        argv: Command-line arguments to parse. If None, uses sys.argv[1:].

    Returns:
        Result string produced by executing the calculation.
    """
    return exec(SpeedSkatingParser(argv=argv), SpeedSkatingStats)


if __name__ == "__main__":
    print(main())
