import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.planet import Planet
from la_haut.domain.sighting import Sighting
from tests.support.builders import DEFAULT_INSTANT, a_planet_position


def seen_toward(direction):
    return Sighting(at=DEFAULT_INSTANT, direction=direction)


def test_the_four_planets_mistaken_for_satellites_are_known():
    assert set(Planet) == {Planet.VENUS, Planet.MARS, Planet.JUPITER, Planet.SATURN}


def test_a_planet_in_the_given_direction_matches_with_its_angle_to_that_direction():
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=280.0)

    assert venus.angle_to(seen_toward(CompassPoint.WEST)) == pytest.approx(10.0)


def test_a_planet_in_a_neighbouring_direction_still_matches_further_away():
    jupiter = a_planet_position(azimuth_deg=206.0)

    assert jupiter.angle_to(seen_toward(CompassPoint.SOUTH)) == pytest.approx(26.0)


def test_the_angle_is_measured_across_the_north():
    assert a_planet_position(azimuth_deg=350.0).angle_to(
        seen_toward(CompassPoint.NORTH)
    ) == pytest.approx(10.0)


def test_a_planet_in_another_direction_does_not_match():
    assert a_planet_position(azimuth_deg=90.0).angle_to(seen_toward(CompassPoint.WEST)) is None


def test_a_planet_below_the_horizon_does_not_match():
    hidden = a_planet_position(azimuth_deg=270.0, elevation_deg=-2.0)

    assert hidden.angle_to(seen_toward(CompassPoint.WEST)) is None


def test_a_planet_in_a_sky_still_too_bright_does_not_match():
    at_dusk = a_planet_position(azimuth_deg=270.0, sun_elevation_deg=-3.0)

    assert at_dusk.angle_to(seen_toward(CompassPoint.WEST)) is None
