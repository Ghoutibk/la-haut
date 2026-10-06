from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from la_haut.composition import (
    build_identify_sighting_from_celestrak,
    build_list_visible_passes_from_celestrak,
    build_web_app,
)
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.planet import Planet
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
    ROCKET_BODY_NAME,
    ROCKET_BODY_TLE_LINE_1,
    ROCKET_BODY_TLE_LINE_2,
    STARLINK_TRAIN,
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
        best, *_ = identify_sighting.execute(an_observer_in_paris(), seen_at_its_highest).candidates

    assert best.satellite_name == ISS_NAME


def test_the_web_app_is_assembled_on_the_celestrak_catalog(tmp_path):
    with FakeCelestrak() as celestrak:
        app = build_web_app(tmp_path / "visual.tle", base_url=celestrak.url)

        response = TestClient(app).get("/")

    assert response.status_code == 200


def test_the_recent_starlinks_from_celestrak_are_announced_as_a_train(tmp_path):
    day_after_epoch = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(days=1))
    rocket_body = (ROCKET_BODY_NAME, ROCKET_BODY_TLE_LINE_1, ROCKET_BODY_TLE_LINE_2)
    starlinks = [line for entry in STARLINK_TRAIN for line in entry]

    with FakeCelestrak() as celestrak:
        celestrak.publishes(*rocket_body, group="visual")
        celestrak.publishes(*starlinks, *rocket_body, group="last-30-days")
        list_visible_passes = build_list_visible_passes_from_celestrak(
            tmp_path / "visual.tle", base_url=celestrak.url
        )
        [train] = list_visible_passes.execute(an_observer_in_paris(), day_after_epoch)

    assert (train.is_starlink_train, train.train_size) == (True, 3)
    assert (tmp_path / "last-30-days.tle").exists()


def test_a_planet_is_identified_when_no_famous_satellite_was_there(tmp_path):
    venus_at_dusk = Sighting(
        at=datetime(2018, 7, 3, 20, 45, tzinfo=UTC), direction=CompassPoint.WEST
    )

    with FakeCelestrak() as celestrak:
        celestrak.publishes(ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2)
        identify_sighting = build_identify_sighting_from_celestrak(
            tmp_path / "visual.tle", base_url=celestrak.url
        )
        [candidate] = identify_sighting.execute(an_observer_in_paris(), venus_at_dusk).candidates

    assert candidate.planet == Planet.VENUS
