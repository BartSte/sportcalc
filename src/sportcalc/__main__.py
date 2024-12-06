from sportcalc.core.cli.parser import make_top_level_parser

if __name__ == "__main__":
    parser = make_top_level_parser()
    parser.print_help()
