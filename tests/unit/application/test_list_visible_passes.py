from datetime import timedelta

from la_haut.application.list_visible_passes import ListVisiblePasses
from tests.support.builders import (
    DEFAULT_INSTANT,
    a_satellite,
    a_track,
    an_evening,
    an_observer_in_paris,
)
from tests.support.fakes import FakeSatelliteCatalog, FakeSkyTracker

LATER = DEFAULT_INSTANT + timedelta(minutes=30)


def list_visible_passes(satellites, tracks_by_name, tracker=None):
    tracker = tracker or FakeSkyTracker(tracks_by_name)
    use_case = ListVisiblePasses(catalog=FakeSatelliteCatalog(satellites), tracker=tracker)
    return use_case.execute(an_observer_in_paris(), an_evening())


def test_nothing_is_listed_when_no_satellite_is_tracked():
    assert list_visible_passes([], {}) == []


def test_the_passes_of_every_tracked_satellite_are_listed_in_chronological_order():
    passes = list_visible_passes(
        [a_satellite("ISS"), a_satellite("STARLINK-G10")],
        {"ISS": a_track({}, {}, start=LATER), "STARLINK-G10": a_track({}, {})},
    )

    assert [visible_pass.satellite_name for visible_pass in passes] == ["STARLINK-G10", "ISS"]


def test_each_satellite_is_tracked_for_the_given_observer_and_window():
    tracker = FakeSkyTracker({})

    list_visible_passes([a_satellite("ISS")], {}, tracker=tracker)

    assert tracker.requests == [("ISS", an_observer_in_paris(), an_evening())]
