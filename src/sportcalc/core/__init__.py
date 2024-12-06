from os.path import dirname, join

from sportcalc.core.execute import exec

static: str = join(dirname(__file__), "static")

__all__ = ["exec", "static"]
