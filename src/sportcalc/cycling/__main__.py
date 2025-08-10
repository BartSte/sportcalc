from sportcalc._core import exec

from sportcalc.cycling.parser import CyclingParser
from sportcalc.cycling.stats import CyclingStats


def main(argv: list[str] | None = None) -> str:
    """Run the cycling CLI entrypoint.

    Args:
        argv: Command-line arguments to parse. If None, sys.argv[1:] is used.

    Returns:
        The formatted results string produced by the CLI execution.
    """
    return exec(CyclingParser(argv=argv), CyclingStats)


if __name__ == "__main__":
    print(main())
