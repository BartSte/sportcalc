from os.path import dirname, join

from sportcalc.cycling.__main__ import main

static: str = join(dirname(__file__), "static")

__all__ = ["main", "static"]
