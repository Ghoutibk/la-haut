from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.pass_detection import detect_visible_passes
from la_haut.domain.visibility import NakedEyeVisibility
from tests.support.builders import DEFAULT_INSTANT, ONE_MINUTE, a_track

IN_SHADOW = {"is_sunlit": False}
BELOW_HORIZON = {"elevation_deg": -5.0}


def detect(track):
    return detect_visible_passes("ISS", track, NakedEyeVisibility())


def test_no_samples_means_no_pass():
    assert detect([]) == []


def test_a_track_that_is_never_visible_gives_no_pass():
    assert detect(a_track(IN_SHADOW, BELOW_HORIZON, IN_SHADOW)) == []


def test_a_visible_run_becomes_one_pass_from_its_first_to_its_last_visible_sample():
    track = a_track(
        IN_SHADOW,
        {"azimuth_deg": 270.0, "elevation_deg": 12.0},
        {"azimuth_deg": 200.0, "elevation_deg": 60.0},
        {"azimuth_deg": 135.0, "elevation_deg": 15.0},
        BELOW_HORIZON,
    )

    [visible_pass] = detect(track)

    assert visible_pass.satellite_name == "ISS"
    assert visible_pass.starts_at == DEFAULT_INSTANT + ONE_MINUTE
    assert visible_pass.ends_at == DEFAULT_INSTANT + 3 * ONE_MINUTE
    assert visible_pass.appears_in == CompassPoint.WEST
    assert visible_pass.vanishes_in == CompassPoint.SOUTH_EAST
    assert visible_pass.max_elevation_deg == 60.0


def test_a_pass_lasts_from_its_first_to_its_last_visible_sample():
    [visible_pass] = detect(a_track({}, {}, {}))

    assert visible_pass.duration == 2 * ONE_MINUTE


def test_two_visible_runs_separated_by_a_shadow_give_two_passes_in_order():
    first, second = detect(a_track({}, IN_SHADOW, {}, {}))

    assert first.starts_at == DEFAULT_INSTANT
    assert second.starts_at == DEFAULT_INSTANT + 2 * ONE_MINUTE


def test_a_pass_still_visible_on_the_last_sample_is_kept():
    [visible_pass] = detect(a_track(IN_SHADOW, {}, {}))

    assert visible_pass.ends_at == DEFAULT_INSTANT + 2 * ONE_MINUTE


def test_a_pass_keeps_its_visible_path_through_the_sky():
    track = a_track(IN_SHADOW, {"azimuth_deg": 200.0}, {"azimuth_deg": 150.0}, BELOW_HORIZON)

    [visible_pass] = detect(track)

    assert visible_pass.path == (track[1], track[2])
