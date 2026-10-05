from la_haut.application.famous_satellite_catalog import FamousSatelliteCatalog
from tests.support.builders import a_satellite
from tests.support.fakes import FakeSatelliteCatalog
from tests.support.fixtures import (
    HUBBLE_NAME,
    HUBBLE_TLE_LINE_1,
    HUBBLE_TLE_LINE_2,
    ISS_NAME,
    ROCKET_BODY_NAME,
    ROCKET_BODY_TLE_LINE_1,
    ROCKET_BODY_TLE_LINE_2,
)


def test_only_the_famous_satellites_of_a_catalog_are_tracked_in_their_order():
    iss = a_satellite(ISS_NAME)
    rocket_body = a_satellite(ROCKET_BODY_NAME, (ROCKET_BODY_TLE_LINE_1, ROCKET_BODY_TLE_LINE_2))
    hubble = a_satellite(HUBBLE_NAME, (HUBBLE_TLE_LINE_1, HUBBLE_TLE_LINE_2))

    catalog = FamousSatelliteCatalog(FakeSatelliteCatalog([iss, rocket_body, hubble]))

    assert catalog.tracked_satellites() == [iss, hubble]
