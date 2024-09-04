from os.path import join
from typing import Any

from core.cli.printer import make_input_text
from cycling import paths
from cycling.stats import CyclingStats


def print_summary(data: CyclingStats) -> str:
    """

    Args:
        data:

    Returns:

    """
    as_dict: dict[str, Any] = data.as_dict()
    template: str = join(paths.static, "results.template")
    with open(template) as results_file:
        inputs_text = make_input_text(as_dict)
        results_text = results_file.read().format(**as_dict)
        return inputs_text + results_text
