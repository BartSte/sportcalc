import json
from os.path import join
from typing import Any

from core import paths
from core.stats import ExerciseStats


def make_input_text(data: dict[str, Any]) -> str:
    """TODO

    Args:
        data:

    Returns:

    """
    inputs: str = join(paths.static, "inputs.template")
    with open(inputs) as inputs_file:
        return inputs_file.read().format(**data)


def dump_json(data: ExerciseStats, indent: int = 4, **kwargs: Any) -> str:
    """TODO

    Args:
        data:
        **kwargs:

    Returns:

    """
    # TODO exclude non-SI from json
    # non_si_units: tuple[str, ...] = "kj", "kmph", "km"
    # exclude_non_si = [x for x in dir(self) if x.endswith(non_si_units)]
    # exclude.extend(exclude_non_si)
    # TODO make a serializer for time
    as_dict: dict[str, Any] = data.as_dict()
    as_dict["time"] = as_dict["time"].strftime("%H:%M:%S")
    return json.dumps(as_dict, indent=indent, **kwargs)
