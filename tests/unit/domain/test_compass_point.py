import pytest

from la_haut.domain.compass_point import CompassPoint, InvalidAzimuthError


@pytest.mark.parametrize(
    ("azimuth_deg", "expected"),
    [
        (0, CompassPoint.NORTH),
        (45, CompassPoint.NORTH_EAST),
        (90, CompassPoint.EAST),
        (135, CompassPoint.SOUTH_EAST),
        (180, CompassPoint.SOUTH),
        (225, CompassPoint.SOUTH_WEST),
        (270, CompassPoint.WEST),
        (315, CompassPoint.NORTH_WEST),
    ],
)
def test_a_heading_maps_to_its_compass_point(azimuth_deg, expected):
    assert CompassPoint.from_azimuth(azimuth_deg) == expected


@pytest.mark.parametrize(
    ("azimuth_deg", "expected"),
    [
        (22.49, CompassPoint.NORTH),
        (22.5, CompassPoint.NORTH_EAST),
        (337.49, CompassPoint.NORTH_WEST),
        (337.5, CompassPoint.NORTH),
        (359.99, CompassPoint.NORTH),
    ],
)
def test_each_compass_point_covers_45_degrees_centred_on_its_heading(azimuth_deg, expected):
    assert CompassPoint.from_azimuth(azimuth_deg) == expected


@pytest.mark.parametrize("azimuth_deg", [-0.01, 360, 400])
def test_an_azimuth_outside_0_to_360_degrees_is_rejected(azimuth_deg):
    with pytest.raises(InvalidAzimuthError):
        CompassPoint.from_azimuth(azimuth_deg)


@pytest.mark.parametrize(
    ("first", "second"),
    [
        (CompassPoint.SOUTH, CompassPoint.SOUTH),
        (CompassPoint.SOUTH, CompassPoint.SOUTH_EAST),
        (CompassPoint.SOUTH_EAST, CompassPoint.SOUTH),
        (CompassPoint.NORTH, CompassPoint.NORTH_WEST),
    ],
)
def test_a_compass_point_is_close_to_itself_and_its_two_neighbours(first, second):
    assert first.is_close_to(second)


@pytest.mark.parametrize(
    ("first", "second"),
    [
        (CompassPoint.NORTH, CompassPoint.EAST),
        (CompassPoint.SOUTH_EAST, CompassPoint.NORTH_WEST),
    ],
)
def test_a_compass_point_is_not_close_to_points_further_away(first, second):
    assert not first.is_close_to(second)
