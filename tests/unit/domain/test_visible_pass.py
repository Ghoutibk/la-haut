from datetime import timedelta

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.sighting import Sighting
from tests.support.builders import DEFAULT_INSTANT, ONE_MINUTE, a_track, a_visible_pass

SOUTH = {"azimuth_deg": 180.0}
SOUTH_EAST = {"azimuth_deg": 135.0}
EAST = {"azimuth_deg": 90.0}


def a_pass_through(*samples_overrides):
    return a_visible_pass(path=tuple(a_track(*samples_overrides)))


def seen(direction, minutes_after_start=0.0):
    return Sighting(at=DEFAULT_INSTANT + minutes_after_start * ONE_MINUTE, direction=direction)


def test_a_pass_seen_where_it_was_at_that_very_moment_matches_exactly():
    visible_pass = a_pass_through(SOUTH, SOUTH_EAST, EAST)

    assert visible_pass.gap_to(seen(CompassPoint.SOUTH_EAST, 1)) == timedelta(0)


def test_a_direction_given_roughly_still_matches():
    visible_pass = a_pass_through(SOUTH, SOUTH_EAST, EAST)

    assert visible_pass.gap_to(seen(CompassPoint.SOUTH_WEST, 0)) == timedelta(0)


def test_the_gap_is_measured_to_the_closest_matching_moment():
    visible_pass = a_pass_through(SOUTH, SOUTH_EAST, EAST)

    assert visible_pass.gap_to(seen(CompassPoint.EAST, 4)) == 2 * ONE_MINUTE


def test_a_pass_never_seen_in_that_direction_does_not_match():
    visible_pass = a_pass_through(SOUTH, SOUTH_EAST, EAST)

    assert visible_pass.gap_to(seen(CompassPoint.NORTH_WEST, 1)) is None


def test_a_pass_more_than_five_minutes_away_from_the_sighting_does_not_match():
    visible_pass = a_pass_through(SOUTH, SOUTH_EAST, EAST)

    assert visible_pass.gap_to(seen(CompassPoint.EAST, 7.5)) is None
