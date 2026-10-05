from datetime import timedelta

from la_haut.domain.docked_passes import merge_docked_passes
from tests.support.builders import ONE_MINUTE, a_visible_pass

A_FEW_SECONDS = timedelta(seconds=10)


def test_no_passes_means_nothing_to_merge():
    assert merge_docked_passes([]) == []


def test_a_lone_pass_is_kept_as_it_is():
    lone_pass = a_visible_pass()

    assert merge_docked_passes([lone_pass]) == [lone_pass]


def test_objects_docked_together_become_one_pass_named_after_the_first_listed():
    station = a_visible_pass(satellite_name="CSS (TIANHE)")
    module = a_visible_pass(
        satellite_name="CSS (WENTIAN)", starts_at=station.starts_at + A_FEW_SECONDS
    )
    vehicle = a_visible_pass(satellite_name="SHENZHOU-23", ends_at=station.ends_at - A_FEW_SECONDS)

    [merged] = merge_docked_passes([station, module, vehicle])

    assert merged.satellite_name == "CSS (TIANHE)"
    assert merged.docked_with == ("CSS (WENTIAN)", "SHENZHOU-23")
    assert (merged.starts_at, merged.ends_at) == (station.starts_at, station.ends_at)


def test_passes_at_different_times_stay_separate():
    early = a_visible_pass(satellite_name="ISS (ZARYA)")
    later = a_visible_pass(
        satellite_name="CSS (TIANHE)",
        starts_at=early.starts_at + 10 * ONE_MINUTE,
        ends_at=early.ends_at + 10 * ONE_MINUTE,
    )

    assert merge_docked_passes([early, later]) == [early, later]


def test_passes_starting_together_but_ending_apart_stay_separate():
    short = a_visible_pass(satellite_name="ISS (ZARYA)")
    longer = a_visible_pass(satellite_name="HST", ends_at=short.ends_at + 2 * ONE_MINUTE)

    assert merge_docked_passes([short, longer]) == [short, longer]


def test_simultaneous_passes_at_different_heights_in_the_sky_stay_separate():
    low = a_visible_pass(satellite_name="ISS (ZARYA)", max_elevation_deg=17.0)
    high = a_visible_pass(satellite_name="HST", max_elevation_deg=40.0)

    assert merge_docked_passes([low, high]) == [low, high]
