from datetime import time

import pytest
from corecalc.cli.type_parsers import parse_time_with_unit
from corecalc.exceptions import CoreValueError


def test_parse_with_unit():
    assert time(second=1) == parse_time_with_unit("1s")
    assert time(second=1) == parse_time_with_unit("1second")
    assert time(second=1) == parse_time_with_unit("1seconds")
    assert time(second=1) == parse_time_with_unit("1 s")
    assert time(second=1) == parse_time_with_unit("1.5 s")
    assert time(minute=3) == parse_time_with_unit("3m")
    assert time(minute=3) == parse_time_with_unit("3minute")
    assert time(minute=3) == parse_time_with_unit("3minutes")
    assert time(second=30) == parse_time_with_unit("0.5 m")
    assert time(hour=5) == parse_time_with_unit("5h")
    assert time(hour=5) == parse_time_with_unit("5hour")
    assert time(hour=5) == parse_time_with_unit("5hours")
    assert time(minute=30) == parse_time_with_unit("0.5 h")


def test_parse_with_unit_invalid():  # noqa: D103
    invalids = ["1", "1s1", "1_1 h", "1.5", "s", "1sm", "1ms"]
    for invalid in invalids:
        with pytest.raises(CoreValueError):
            results = parse_time_with_unit(invalid)
            pytest.fail(f"Expected CoreValueError for '{invalid}', got {results}")
