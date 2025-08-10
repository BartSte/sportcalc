import sys

from sportcalc._core.cli.parser import make_top_level_parser


def main() -> None:
    """Run the top-level CLI.

    Parses known arguments with the core parser and dispatches to a selected
    sport subcommand if present. When no subcommand is provided, prints help.

    Returns:
        None: This function does not return a value.
    """
    parser = make_top_level_parser()
    args, _ = parser.parse_known_args()
    if main := getattr(args, "main", None):
        result = main(argv=sys.argv[2:])
        if result is not None:
            print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
