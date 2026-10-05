import pytest

from la_haut.domain.famous_satellites import is_famous
from tests.support.builders import a_satellite
from tests.support.fixtures import (
    HUBBLE_NAME,
    HUBBLE_TLE_LINE_1,
    HUBBLE_TLE_LINE_2,
    ISS_NAME,
    ISS_TLE_LINE_1,
    ISS_TLE_LINE_2,
    ROCKET_BODY_NAME,
    ROCKET_BODY_TLE_LINE_1,
    ROCKET_BODY_TLE_LINE_2,
    TIANGONG_NAME,
    TIANGONG_TLE_LINE_1,
    TIANGONG_TLE_LINE_2,
)


@pytest.mark.parametrize(
    ("name", "lines"),
    [
        (ISS_NAME, (ISS_TLE_LINE_1, ISS_TLE_LINE_2)),
        (TIANGONG_NAME, (TIANGONG_TLE_LINE_1, TIANGONG_TLE_LINE_2)),
        (HUBBLE_NAME, (HUBBLE_TLE_LINE_1, HUBBLE_TLE_LINE_2)),
    ],
)
def test_the_iss_tiangong_and_hubble_are_famous(name, lines):
    assert is_famous(a_satellite(name, lines))


def test_a_rocket_body_is_not_famous_even_when_bright():
    assert not is_famous(
        a_satellite(ROCKET_BODY_NAME, (ROCKET_BODY_TLE_LINE_1, ROCKET_BODY_TLE_LINE_2))
    )


def test_fame_follows_the_norad_number_not_the_name():
    assert not is_famous(a_satellite(ISS_NAME, (ROCKET_BODY_TLE_LINE_1, ROCKET_BODY_TLE_LINE_2)))
