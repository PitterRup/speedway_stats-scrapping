import pytest

from speedway_data_parser.string_tools import int_or_none, strip


@pytest.mark.parametrize(
    "val, exp_val", [("\nabc abc", "abc abc"), ("\tabc abc ", "abc abc"), (" abc abc ", "abc abc"), (None, None)]
)
def test_strip(val, exp_val):
    assert strip(val) == exp_val


@pytest.mark.parametrize("val, exp_val", [("1", 1), ("2fs", None), ("1.2", None), (None, None)])
def test_int_or_none(val, exp_val):
    assert int_or_none(val) == exp_val
