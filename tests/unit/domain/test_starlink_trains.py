from datetime import timedelta

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.starlink_trains import gather_starlink_trains
from tests.support.builders import ONE_MINUTE, a_track, a_visible_pass

FIFTEEN_SECONDS = timedelta(seconds=15)
LAUNCH = "26180"


def a_starlink_pass(name, delay=timedelta(0), **overrides):
    """Un Starlink du lancement LAUNCH, `delay` derrière le premier de la file."""
    leader = a_visible_pass()
    defaults = {
        "launch": LAUNCH,
        "starts_at": leader.starts_at + delay,
        "ends_at": leader.ends_at + delay,
        "path": tuple(a_track({}, {}, start=leader.starts_at + delay)),
    }
    return a_visible_pass(satellite_name=name, **{**defaults, **overrides})


def test_no_passes_means_no_train():
    assert gather_starlink_trains([]) == []


def test_a_lone_starlink_is_not_a_train():
    lone = a_starlink_pass("STARLINK-1")

    [kept] = gather_starlink_trains([lone])

    assert kept == lone
    assert (kept.is_starlink_train, kept.train_size) == (False, 1)


def test_starlinks_of_one_launch_following_each_other_become_one_train():
    leader = a_starlink_pass("STARLINK-1", vanishes_in=CompassPoint.EAST)
    second = a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS)
    last = a_starlink_pass("STARLINK-3", 2 * FIFTEEN_SECONDS, vanishes_in=CompassPoint.NORTH_EAST)

    [train] = gather_starlink_trains([second, leader, last])

    assert train.is_starlink_train
    assert train.train_size == 3
    assert (train.starts_at, train.ends_at) == (leader.starts_at, last.ends_at)
    assert (train.appears_in, train.vanishes_in) == (leader.appears_in, CompassPoint.NORTH_EAST)


def test_a_train_keeps_the_path_of_all_its_satellites_in_time_order():
    leader = a_starlink_pass("STARLINK-1")
    follower = a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS)

    [train] = gather_starlink_trains([follower, leader])

    assert train.path == tuple(sorted((*leader.path, *follower.path), key=lambda s: s.at))


def test_a_train_is_not_a_group_of_docked_objects():
    [train] = gather_starlink_trains(
        [a_starlink_pass("STARLINK-1"), a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS)]
    )

    assert train.docked_with == ()


def test_starlinks_of_different_launches_stay_separate():
    first = a_starlink_pass("STARLINK-1")
    other_launch = a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS, launch="26175")

    assert gather_starlink_trains([first, other_launch]) == [first, other_launch]


def test_another_object_of_the_same_launch_is_not_part_of_the_train():
    starlink = a_starlink_pass("STARLINK-1")
    rocket_body = a_starlink_pass("FALCON 9 R/B", FIFTEEN_SECONDS)

    assert gather_starlink_trains([starlink, rocket_body]) == [starlink, rocket_body]


def test_starlinks_of_one_launch_seen_on_different_orbits_stay_separate():
    early = a_starlink_pass("STARLINK-1")
    next_orbit = a_starlink_pass("STARLINK-2", 95 * ONE_MINUTE)

    assert gather_starlink_trains([early, next_orbit]) == [early, next_orbit]


def test_starlinks_of_one_launch_crossing_the_sky_differently_stay_separate():
    southward = a_starlink_pass("STARLINK-1", appears_in=CompassPoint.NORTH)
    northward = a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS, appears_in=CompassPoint.SOUTH)

    assert gather_starlink_trains([southward, northward]) == [southward, northward]


def test_starlinks_of_one_launch_at_very_different_heights_stay_separate():
    low = a_starlink_pass("STARLINK-1", max_elevation_deg=15.0)
    high = a_starlink_pass("STARLINK-2", FIFTEEN_SECONDS, max_elevation_deg=40.0)

    assert gather_starlink_trains([low, high]) == [low, high]
