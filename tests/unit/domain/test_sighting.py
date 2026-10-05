from datetime import datetime

import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.sighting import InvalidSightingError, Sighting
from tests.support.builders import DEFAULT_INSTANT


def test_a_sighting_is_a_moment_and_a_direction_in_the_sky():
    sighting = Sighting(at=DEFAULT_INSTANT, direction=CompassPoint.WEST)

    assert (sighting.at, sighting.direction) == (DEFAULT_INSTANT, CompassPoint.WEST)


def test_a_sighting_requires_a_timezone_aware_instant():
    with pytest.raises(InvalidSightingError):
        Sighting(at=datetime(2026, 10, 5, 21, 42), direction=CompassPoint.WEST)
