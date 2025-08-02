from collections.abc import Callable
from functools import partial
from os import path

join: Callable[[str], str] = partial(path.join, path.dirname(__file__))
