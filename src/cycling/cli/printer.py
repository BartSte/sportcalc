from os.path import join
from typing import Any

from core.cli.printer import make_input_text
from cycling import paths


def print_summary(data: dict[str, Any]) -> str:
    """

    Args:
        data:

    Returns:

    """
    template: str = join(paths.static, "results.template")
    with open(template) as results_file:
        inputs_text = make_input_text(data)
        results_text = results_file.read().format(**data)
        return inputs_text + results_text
