import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.identification import Identification
from la_haut.domain.planet import Planet
from la_haut.interface.http.presenters import (
    present_candidate,
    present_identification,
    present_pass,
)
from tests.support.builders import (
    DEFAULT_INSTANT,
    ONE_MINUTE,
    a_planet_position,
    a_visible_pass,
)


def test_a_pass_is_presented_with_its_times_in_iso_format():
    presented = present_pass(
        a_visible_pass(starts_at=DEFAULT_INSTANT, ends_at=DEFAULT_INSTANT + 4 * ONE_MINUTE)
    )

    assert presented["starts_at"] == "2026-10-05T19:42:00+00:00"
    assert presented["ends_at"] == "2026-10-05T19:46:00+00:00"
    assert presented["duration_s"] == 240


def test_directions_are_presented_with_their_code_and_french_name():
    presented = present_pass(
        a_visible_pass(appears_in=CompassPoint.SOUTH_WEST, vanishes_in=CompassPoint.NORTH_EAST)
    )

    assert presented["appears_in"] == {"code": "SW", "label": "sud-ouest"}
    assert presented["vanishes_in"] == {"code": "NE", "label": "nord-est"}


def test_the_satellite_its_docked_companions_and_its_rounded_height_are_presented():
    presented = present_pass(
        a_visible_pass(
            satellite_name="CSS (TIANHE)", docked_with=("SHENZHOU-23",), max_elevation_deg=17.4
        )
    )

    assert presented["satellite"] == "CSS (TIANHE)"
    assert presented["docked_with"] == ["SHENZHOU-23"]
    assert presented["max_elevation_deg"] == 17


def test_every_compass_point_has_a_french_name():
    names = {
        present_pass(a_visible_pass(appears_in=point))["appears_in"]["label"]
        for point in CompassPoint
    }

    assert len(names) == len(CompassPoint)


@pytest.mark.parametrize(
    ("catalog_name", "public_name"),
    [
        ("ISS (ZARYA)", "Station spatiale internationale"),
        ("CSS (TIANHE)", "Station spatiale chinoise Tiangong"),
        ("HST", "Télescope spatial Hubble"),
    ],
)
def test_famous_satellites_are_presented_under_their_public_name(catalog_name, public_name):
    assert present_pass(a_visible_pass(satellite_name=catalog_name))["name"] == public_name


def test_another_satellite_keeps_its_catalog_name():
    assert present_pass(a_visible_pass(satellite_name="SL-16 R/B"))["name"] == "SL-16 R/B"


def test_a_starlink_train_is_presented_with_the_number_of_its_satellites():
    presented = present_pass(
        a_visible_pass(
            satellite_name="STARLINK-90001", train_followers=("STARLINK-90002", "STARLINK-90003")
        )
    )

    assert presented["kind"] == "train"
    assert presented["name"] == "Train Starlink (3 satellites)"


def test_a_lone_satellite_is_presented_as_a_satellite():
    assert present_pass(a_visible_pass())["kind"] == "satellite"


@pytest.mark.parametrize(
    ("planet", "french_name"),
    [
        (Planet.VENUS, "Vénus"),
        (Planet.JUPITER, "Jupiter"),
        (Planet.MARS, "Mars"),
        (Planet.SATURN, "Saturne"),
    ],
)
def test_a_planet_is_presented_under_its_french_name(planet, french_name):
    presented = present_candidate(a_planet_position(planet=planet))

    assert (presented["kind"], presented["name"], presented["planet"]) == (
        "planet",
        french_name,
        planet.value,
    )


def test_a_planet_is_presented_with_its_direction_and_rounded_height():
    presented = present_candidate(a_planet_position(azimuth_deg=280.0, elevation_deg=11.6))

    assert presented["direction"] == {"code": "W", "label": "ouest"}
    assert presented["elevation_deg"] == 12


def test_a_satellite_candidate_is_presented_as_its_pass():
    visible_pass = a_visible_pass()

    assert present_candidate(visible_pass) == present_pass(visible_pass)


def test_an_identification_presents_its_candidates_and_whether_the_satellites_were_checked():
    venus = a_planet_position()

    presented = present_identification(
        Identification(candidates=(venus,), satellites_checked=False)
    )

    assert presented == {"candidates": [present_candidate(venus)], "satellites_checked": False}
