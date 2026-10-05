import pytest

from la_haut.application.combined_satellite_catalog import CombinedSatelliteCatalog
from la_haut.application.ports import CatalogUnavailableError
from tests.support.builders import a_satellite
from tests.support.fakes import FakeSatelliteCatalog, UnavailableSatelliteCatalog
from tests.support.fixtures import HUBBLE_NAME, HUBBLE_TLE_LINE_1, HUBBLE_TLE_LINE_2, ISS_NAME

ISS = a_satellite(ISS_NAME)
HUBBLE = a_satellite(HUBBLE_NAME, (HUBBLE_TLE_LINE_1, HUBBLE_TLE_LINE_2))


def test_the_satellites_of_every_catalog_are_tracked_in_order():
    catalog = CombinedSatelliteCatalog(FakeSatelliteCatalog([ISS]), FakeSatelliteCatalog([HUBBLE]))

    assert catalog.tracked_satellites() == [ISS, HUBBLE]


def test_a_satellite_listed_by_two_catalogs_is_tracked_once_as_the_first_one_says():
    renamed_iss = a_satellite("ISS")

    catalog = CombinedSatelliteCatalog(
        FakeSatelliteCatalog([ISS]), FakeSatelliteCatalog([renamed_iss, HUBBLE])
    )

    assert catalog.tracked_satellites() == [ISS, HUBBLE]


def test_an_unavailable_catalog_does_not_hide_the_others():
    catalog = CombinedSatelliteCatalog(UnavailableSatelliteCatalog(), FakeSatelliteCatalog([ISS]))

    assert catalog.tracked_satellites() == [ISS]


def test_the_combination_is_unavailable_when_every_catalog_is():
    catalog = CombinedSatelliteCatalog(UnavailableSatelliteCatalog(), UnavailableSatelliteCatalog())

    with pytest.raises(CatalogUnavailableError):
        catalog.tracked_satellites()
