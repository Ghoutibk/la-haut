from datetime import timedelta

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.sighting import Sighting
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import (
    DEFAULT_INSTANT,
    ONE_MINUTE,
    a_satellite,
    a_track,
    an_observer_in_paris,
)
from tests.support.fakes import FakeSatelliteCatalog, FakeSkyTracker

WEST = {"azimuth_deg": 270.0}
NORTH = {"azimuth_deg": 0.0}
SEEN_IN_THE_WEST = Sighting(at=DEFAULT_INSTANT + 2 * ONE_MINUTE, direction=CompassPoint.WEST)


def identify(tracks_by_name, sighting=SEEN_IN_THE_WEST, tracker=None):
    satellites = [a_satellite(name) for name in tracks_by_name]
    tracker = tracker or FakeSkyTracker(tracks_by_name)
    list_visible_passes = ListVisiblePasses(
        catalog=FakeSatelliteCatalog(satellites), tracker=tracker
    )
    return IdentifySighting(list_visible_passes).execute(an_observer_in_paris(), sighting)


def test_the_satellite_that_was_there_at_that_moment_is_identified():
    [candidate] = identify({"ISS": a_track(WEST, WEST, WEST)})

    assert candidate.satellite_name == "ISS"


def test_nothing_is_identified_when_no_satellite_was_there():
    assert identify({"ISS": a_track(NORTH, NORTH, NORTH)}) == []


def test_candidates_come_from_the_closest_to_the_furthest_in_time():
    candidates = identify(
        {
            "HST": a_track(WEST, NORTH, NORTH, NORTH, NORTH),
            "ISS": a_track(NORTH, NORTH, WEST, NORTH, NORTH),
        }
    )

    assert [candidate.satellite_name for candidate in candidates] == ["ISS", "HST"]


def test_the_sky_is_searched_five_minutes_around_the_sighting():
    tracker = FakeSkyTracker({})

    identify({"ISS": []}, tracker=tracker)

    [(_, _, window)] = tracker.requests
    five_minutes = timedelta(minutes=5)
    assert window == TimeWindow(
        SEEN_IN_THE_WEST.at - five_minutes, SEEN_IN_THE_WEST.at + five_minutes
    )
