import pytest

from la_haut.domain.starlink import is_starlink


@pytest.mark.parametrize("name", ["STARLINK-1007", "STARLINK-90001"])
def test_a_starlink_is_recognized_by_its_catalog_name(name):
    assert is_starlink(name)


@pytest.mark.parametrize("name", ["ISS (ZARYA)", "ONEWEB-0012", "FALCON 9 R/B"])
def test_other_satellites_are_not_starlinks(name):
    assert not is_starlink(name)
