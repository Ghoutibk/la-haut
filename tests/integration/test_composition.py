from datetime import UTC, datetime, timedelta

from la_haut.composition import (
    build_identify_sighting_from_celestrak,
    build_list_visible_passes_from_celestrak,
)
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.sighting import Sighting
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import an_observer_in_paris
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import (
    DOCKED_VEHICLE_NAME,
    DOCKED_VEHICLE_TLE_LINE_1,
    DOCKED_VEHICLE_TLE_LINE_2,
    ISS_NAME,
    ISS_TLE_EPOCH,
    ISS_TLE_LINE_1,
    ISS_TLE_LINE_2,
)


def test_only_the_famous_satellites_from_celestrak_are_announced(tmp_path):
    day_after_epoch = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(days=1))

    with FakeCelestrak() as celestrak:
        celestrak.publishes(
            ISS_NAME,
            ISS_TLE_LINE_1,
            ISS_TLE_LINE_2,
            DOCKED_VEHICLE_NAME,
            DOCKED_VEHICLE_TLE_LINE_1,
            DOCKED_VEHICLE_TLE_LINE_2,
        )
        list_visible_passes = build_list_visible_passes_from_celestrak(
            tmp_path / "visual.tle", base_url=celestrak.url
        )
        [iss_pass] = list_visible_passes.execute(an_observer_in_paris(), day_after_epoch)

    assert (iss_pass.satellite_name, iss_pass.docked_with) == (ISS_NAME, ())


def test_a_sighting_is_identified_among_the_famous_satellites_from_celestrak(tmp_path):
    seen_at_its_highest = Sighting(
        at=datetime(2018, 7, 4, 2, 56, tzinfo=UTC), direction=CompassPoint.SOUTH_EAST
    )

    with FakeCelestrak() as celestrak:
        celestrak.publishes(ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2)
        identify_sighting = build_identify_sighting_from_celestrak(
            tmp_path / "visual.tle", base_url=celestrak.url
        )
        [candidate] = identify_sighting.execute(an_observer_in_paris(), seen_at_its_highest)

    assert candidate.satellite_name == ISS_NAME
