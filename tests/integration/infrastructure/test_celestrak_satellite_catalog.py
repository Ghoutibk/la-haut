import pytest

from la_haut.infrastructure.celestrak_satellite_catalog import CelestrakSatelliteCatalog
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2


@pytest.fixture
def celestrak():
    with FakeCelestrak() as fake:
        fake.publishes(ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2)
        yield fake


@pytest.fixture
def cache_path(tmp_path):
    return tmp_path / "visual.tle"


def a_catalog(celestrak, cache_path):
    return CelestrakSatelliteCatalog(cache_path, base_url=celestrak.url)


def test_without_a_cache_the_brightest_satellites_group_is_downloaded(celestrak, cache_path):
    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert celestrak.requests == [{"GROUP": ["visual"], "FORMAT": ["tle"]}]
    assert cache_path.exists()
