from saulify import common
import pytest

@pytest.mark.parametrize("input,expected", [
    (0, "0"),
    (61, "Z"),
    (62, "10"),
    (3141592, "dbgQ"),
])
def test_get_slug_from_id(input, expected):
    assert common.get_slug_from_int(input) == expected

@pytest.mark.parametrize("input,expected", [
    ("0", 0),
    ("Z", 61),
    ("10", 62),
    ("dbgQ", 3141592),
])
def test_get_slug_from_id(input, expected):
    assert common.get_int_from_slug(input) == expected


