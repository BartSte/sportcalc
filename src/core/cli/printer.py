from os.path import join
from typing import Any

from core import paths


def make_input_text(data: dict[str, Any]) -> str:
    """TODO

    Args:
        data:

    Returns:

    """
    inputs: str = join(paths.static, "inputs.template")
    with open(inputs) as inputs_file:
        return inputs_file.read().format(**data)
