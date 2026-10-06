import itertools
from datetime import UTC, datetime, timedelta

import pytest

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.orbit_mean_elements import OrbitMeanElements
from la_haut.domain.pass_detection import detect_visible_passes
from la_haut.domain.satellite import Satellite
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visibility import NakedEyeVisibility
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from tests.support.builders import a_satellite, an_observer_in_paris
from tests.support.fixtures import ISS_2026_OMM, ISS_NAME, ISS_TLE_EPOCH

STEP = timedelta(seconds=10)

# Valeurs de référence obtenues avec EarthSatellite.find_events de Skyfield (seuil 10°),
# un chemin de calcul indépendant de l'échantillonnage du tracker.
REFERENCE_PASS_START = datetime(2018, 7, 4, 2, 54, 10, tzinfo=UTC)
REFERENCE_PASS_END = datetime(2018, 7, 4, 2, 57, 55, tzinfo=UTC)
REFERENCE_PASS_MAX_ELEVATION_DEG = 14.4
ELEVATION_TOLERANCE_DEG = 0.5

# Avec find_events de Skyfield (horizon à 0°) : après l'époque du TLE, l'ISS ne se lève sur Paris
# qu'à 02:51:26 et se couche à 03:00:40. Le Soleil y est à -7,69° à 02:56:00 UTC (Skyfield).
REFERENCE_RISE = datetime(2018, 7, 4, 2, 51, 26, tzinfo=UTC)
REFERENCE_SET = datetime(2018, 7, 4, 3, 0, 40, tzinfo=UTC)
REFERENCE_SUN_ELEVATION_AT_0256_DEG = -7.69

# Culmination de l'ISS sur Paris trouvée par EarthSatellite.find_events de Skyfield à partir du
# TLE du 6 octobre 2026 : le même jeu d'éléments que l'OMM, par un autre chemin de calcul.
REFERENCE_2026_CULMINATION = datetime(2026, 10, 6, 13, 10, 5, tzinfo=UTC)
REFERENCE_2026_CULMINATION_ELEVATION_DEG = 63.8


@pytest.fixture(scope="module")
def tracker():
    return SkyfieldSkyTracker(step=STEP)


def test_no_sample_is_computed_while_the_satellite_stays_below_the_horizon(tracker):
    an_hour_after_epoch = TimeWindow(
        starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(hours=1)
    )

    assert tracker.track(a_satellite(), an_observer_in_paris(), an_hour_after_epoch) == []


def test_a_pass_is_sampled_at_the_tracker_step_from_below_the_horizon_to_below_it(tracker):
    the_night = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(hours=8))

    track = tracker.track(a_satellite(), an_observer_in_paris(), the_night)

    instants = [sample.at for sample in track]
    assert all(later - earlier == STEP for earlier, later in itertools.pairwise(instants))
    assert track[0].elevation_deg < 0 and track[-1].elevation_deg < 0
    above = [sample for sample in track if sample.elevation_deg > 0]
    assert abs(above[0].at - REFERENCE_RISE) <= STEP
    assert abs(above[-1].at - REFERENCE_SET) <= STEP


def test_each_sample_tells_how_high_the_sun_stands_over_the_observer(tracker):
    at_0256 = datetime(2018, 7, 4, 2, 56, tzinfo=UTC)
    during_the_pass = TimeWindow(
        starts_at=datetime(2018, 7, 4, 2, 50, tzinfo=UTC),
        ends_at=datetime(2018, 7, 4, 3, 5, tzinfo=UTC),
    )

    track = tracker.track(a_satellite(), an_observer_in_paris(), during_the_pass)

    [sample] = [sample for sample in track if sample.at == at_0256]
    assert sample.sun_elevation_deg == pytest.approx(REFERENCE_SUN_ELEVATION_AT_0256_DEG, abs=0.01)


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


def test_a_satellite_known_by_its_omm_is_tracked_where_its_tle_puts_it(tracker):
    iss = Satellite(name=ISS_NAME, elements=OrbitMeanElements.from_fields(ISS_2026_OMM))
    five_minutes = timedelta(minutes=5)
    around_the_culmination = TimeWindow(
        starts_at=REFERENCE_2026_CULMINATION - five_minutes,
        ends_at=REFERENCE_2026_CULMINATION + five_minutes,
    )

    track = tracker.track(iss, an_observer_in_paris(), around_the_culmination)

    highest = max(track, key=lambda sample: sample.elevation_deg)
    assert abs(highest.at - REFERENCE_2026_CULMINATION) <= STEP
    assert highest.elevation_deg == pytest.approx(
        REFERENCE_2026_CULMINATION_ELEVATION_DEG, abs=ELEVATION_TOLERANCE_DEG
    )
