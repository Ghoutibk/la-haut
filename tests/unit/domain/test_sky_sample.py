from datetime import datetime

import pytest

from la_haut.domain.compass_point import CompassPoint, InvalidAzimuthError
from la_haut.domain.sky_sample import InvalidSkySampleError
from tests.support.builders import a_sky_sample


def test_a_sample_knows_the_compass_point_it_is_seen_in():
    sample = a_sky_sample(azimuth_deg=135.0)

    assert sample.direction == CompassPoint.SOUTH_EAST


def test_a_sample_requires_a_timezone_aware_instant():
    with pytest.raises(InvalidSkySampleError):
        a_sky_sample(at=datetime(2026, 10, 5, 21, 42))


@pytest.mark.parametrize("elevation_deg", [-90.01, 90.01])
def test_a_sample_rejects_an_elevation_outside_minus_90_to_90_degrees(elevation_deg):
    with pytest.raises(InvalidSkySampleError):
        a_sky_sample(elevation_deg=elevation_deg)


def test_a_sample_rejects_an_invalid_azimuth():
    with pytest.raises(InvalidAzimuthError):
        a_sky_sample(azimuth_deg=360.0)
