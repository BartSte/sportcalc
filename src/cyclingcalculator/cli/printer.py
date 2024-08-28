from typing import Any

from cyclingcalculator.cli.templates import inputs, results


def print_summary(data: dict[str, Any]) -> str:
    """

    Args:
        data: 

    Returns:
        
    """
    with open(inputs) as inputs_file, open(results) as results_file:
        inputs_text = inputs_file.read().format(**data)
        results_text = results_file.read().format(**data)
        return inputs_text + results_text
