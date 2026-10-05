from datetime import UTC, datetime, timedelta

import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.pass_detection import detect_visible_passes
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visibility import NakedEyeVisibility
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from tests.support.builders import a_satellite, an_observer_in_paris
from tests.support.fixtures import ISS_TLE_EPOCH

STEP = timedelta(seconds=10)

# Valeurs de référence obtenues avec EarthSatellite.find_events de Skyfield (seuil 10°),
# un chemin de calcul indépendant de l'échantillonnage du tracker.
REFERENCE_PASS_START = datetime(2018, 7, 4, 2, 54, 10, tzinfo=UTC)
REFERENCE_PASS_END = datetime(2018, 7, 4, 2, 57, 55, tzinfo=UTC)
REFERENCE_PASS_MAX_ELEVATION_DEG = 14.4
ELEVATION_TOLERANCE_DEG = 0.5


@pytest.fixture(scope="module")
def tracker():
    return SkyfieldSkyTracker(step=STEP)


def test_samples_cover_the_window_at_the_tracker_step(tracker):
    window = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(minutes=1))

    samples = tracker.track(a_satellite(), an_observer_in_paris(), window)

    assert [sample.at for sample in samples] == [ISS_TLE_EPOCH + n * STEP for n in range(6)]


def test_the_sun_stands_about_64_degrees_over_paris_at_noon_in_early_july(tracker):
    noon = datetime(2018, 7, 3, 12, 0, tzinfo=UTC)
    window = TimeWindow(starts_at=noon, ends_at=noon + STEP)

    [sample] = tracker.track(a_satellite(), an_observer_in_paris(), window)

    assert sample.sun_elevation_deg == pytest.approx(64.06, abs=0.1)


def test_tracking_then_detection_finds_the_one_visible_iss_pass_of_that_night(tracker):
    day_after_epoch = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(days=1))
    track = tracker.track(a_satellite(), an_observer_in_paris(), day_after_epoch)

    [visible_pass] = detect_visible_passes("ISS", track, NakedEyeVisibility())

    assert abs(visible_pass.starts_at - REFERENCE_PASS_START) <= STEP
    assert abs(visible_pass.ends_at - REFERENCE_PASS_END) <= STEP
    assert visible_pass.max_elevation_deg == pytest.approx(
        REFERENCE_PASS_MAX_ELEVATION_DEG, abs=ELEVATION_TOLERANCE_DEG
    )
    assert (visible_pass.appears_in, visible_pass.vanishes_in) == (
        CompassPoint.SOUTH,
        CompassPoint.EAST,
    )
