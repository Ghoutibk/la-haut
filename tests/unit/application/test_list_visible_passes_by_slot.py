from datetime import UTC, datetime, timedelta

from la_haut.application.list_visible_passes_by_slot import ListVisiblePassesBySlot
from la_haut.domain.observer import Observer
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import DEFAULT_INSTANT, a_visible_pass, an_observer_in_paris
from tests.support.fakes import FakeVisiblePassesListing

TWELVE_HOURS = timedelta(hours=12)
LYON = Observer(latitude_deg=45.76, longitude_deg=4.84)


def tonight_from(start):
    return TimeWindow(starts_at=start, ends_at=start + TWELVE_HOURS)


def at(hour, minute, day=5):
    return datetime(2026, 10, day, hour, minute, tzinfo=UTC)


def test_the_passes_are_computed_for_the_whole_quarter_hours_of_the_visit():
    listing = FakeVisiblePassesListing([])

    ListVisiblePassesBySlot(listing).execute(an_observer_in_paris(), tonight_from(at(19, 42)))

    assert listing.requests == [
        (an_observer_in_paris(), TimeWindow(starts_at=at(19, 30), ends_at=at(7, 45, day=6)))
    ]


def test_a_second_visit_in_the_same_quarter_hour_is_answered_without_computing_again():
    listing = FakeVisiblePassesListing([])
    by_slot = ListVisiblePassesBySlot(listing)

    by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 42)))
    by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 44)))

    assert len(listing.requests) == 1


def test_a_visit_in_the_next_quarter_hour_computes_again():
    listing = FakeVisiblePassesListing([])
    by_slot = ListVisiblePassesBySlot(listing)

    by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 42)))
    by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 46)))

    assert len(listing.requests) == 2


def test_another_observer_gets_its_own_passes():
    listing = FakeVisiblePassesListing([])
    by_slot = ListVisiblePassesBySlot(listing)

    by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 42)))
    by_slot.execute(LYON, tonight_from(at(19, 42)))

    assert [observer for observer, _ in listing.requests] == [an_observer_in_paris(), LYON]


def test_each_visit_only_gets_the_passes_of_its_own_window():
    over = a_visible_pass(starts_at=at(19, 31), ends_at=at(19, 35))
    ongoing = a_visible_pass(starts_at=at(19, 40), ends_at=at(19, 44))
    too_late = a_visible_pass(starts_at=at(7, 43, day=6), ends_at=at(7, 44, day=6))
    by_slot = ListVisiblePassesBySlot(FakeVisiblePassesListing([over, ongoing, too_late]))

    assert by_slot.execute(an_observer_in_paris(), tonight_from(at(19, 42))) == [ongoing]


def test_the_oldest_slots_are_forgotten_beyond_the_capacity():
    listing = FakeVisiblePassesListing([])
    by_slot = ListVisiblePassesBySlot(listing, capacity=1)

    by_slot.execute(an_observer_in_paris(), tonight_from(DEFAULT_INSTANT))
    by_slot.execute(LYON, tonight_from(DEFAULT_INSTANT))
    by_slot.execute(an_observer_in_paris(), tonight_from(DEFAULT_INSTANT))

    assert len(listing.requests) == 3
