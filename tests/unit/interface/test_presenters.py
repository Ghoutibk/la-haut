import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.interface.http.presenters import present_pass
from tests.support.builders import DEFAULT_INSTANT, ONE_MINUTE, a_visible_pass


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
