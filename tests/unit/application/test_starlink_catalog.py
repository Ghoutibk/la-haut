from la_haut.application.starlink_catalog import StarlinkCatalog
from tests.support.builders import a_satellite
from tests.support.fakes import FakeSatelliteCatalog
from tests.support.fixtures import (
    ROCKET_BODY_NAME,
    ROCKET_BODY_TLE_LINE_1,
    ROCKET_BODY_TLE_LINE_2,
    STARLINK_TRAIN,
)


def test_only_the_starlinks_of_a_catalog_are_tracked_in_their_order():
    first, second, _ = (a_satellite(name, (l1, l2)) for name, l1, l2 in STARLINK_TRAIN)
    rocket_body = a_satellite(ROCKET_BODY_NAME, (ROCKET_BODY_TLE_LINE_1, ROCKET_BODY_TLE_LINE_2))

    catalog = StarlinkCatalog(FakeSatelliteCatalog([first, rocket_body, second]))

    assert catalog.tracked_satellites() == [first, second]
