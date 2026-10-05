from la_haut.domain.visibility import NakedEyeVisibility
from tests.support.builders import a_sky_sample

visibility = NakedEyeVisibility()


def test_a_sunlit_satellite_high_in_a_dark_sky_is_visible():
    assert visibility.allows(a_sky_sample(is_sunlit=True, elevation_deg=45, sun_elevation_deg=-12))


def test_a_satellite_in_the_earth_shadow_is_not_visible():
    assert not visibility.allows(a_sky_sample(is_sunlit=False))


def test_a_satellite_too_close_to_the_horizon_is_not_visible():
    assert not visibility.allows(a_sky_sample(elevation_deg=9.9))


def test_a_satellite_exactly_at_the_minimum_elevation_is_visible():
    assert visibility.allows(a_sky_sample(elevation_deg=10.0))


def test_a_satellite_is_not_visible_while_the_sky_is_still_too_bright():
    assert not visibility.allows(a_sky_sample(sun_elevation_deg=-5.9))


def test_a_satellite_is_visible_from_the_end_of_civil_twilight():
    assert visibility.allows(a_sky_sample(sun_elevation_deg=-6.0))
