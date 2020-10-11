import pytest

from speedway_data_parser import util


@pytest.mark.parametrize('lst, exp_result', [
    ([], None),
    ([1], 1),
])
def test_catch_exceptions(lst, exp_result):
    @util.catch_exceptions(IndexError)
    def f(lst):
        return lst[0]

    try:
        assert f(lst) == exp_result
    except IndexError:
        assert False, u'Wyjątek nie został przechwycony'
