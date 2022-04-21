import pytest


def div_function(a, b):
    if b == 0:
        raise ZeroDivisionError('nie dziel przez 0')
    return a / b


@pytest.mark.parametrize('a, b, result', (
        (0, 9, 0),
        (0, 0, 0),
        (1, 0, 1),
        (1, 1, 1),
        (4, 2, 2)
))
def test_div_function_by_0(a, b, result):
    with pytest.raises(ZeroDivisionError):
        di

    assert div_function(a, b) == result
