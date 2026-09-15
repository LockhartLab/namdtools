import pytest

from namdtools import get_pme_size


def _prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


@pytest.mark.parametrize("a", [1, 2, 8, 10, 27, 32, 68, 99.5, 100])
def test_get_pme_size_only_has_small_factors(a):
    size = get_pme_size(a)
    assert _prime_factors(size) <= {2, 3, 5}


@pytest.mark.parametrize("a", [1, 2, 8, 10, 27, 32, 68, 99.5, 100])
def test_get_pme_size_at_least_input(a):
    size = get_pme_size(a)
    assert size >= a


def test_get_pme_size_rounds_up_decimals():
    # 65 is not smooth (5 * 13), 66 = 2*3*11, ..., 72 = 2^3 * 3^2 is the next smooth number
    assert get_pme_size(68.0) == 72


def test_get_pme_size_already_smooth():
    # 64 = 2^6 is already smooth, so it should be returned unchanged
    assert get_pme_size(64) == 64
