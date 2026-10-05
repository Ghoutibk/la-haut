import os
import time

import pytest

from la_haut.application.ports import CatalogUnavailableError
from la_haut.infrastructure.celestrak_satellite_catalog import CelestrakSatelliteCatalog
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2

THREE_HOURS_S = 3 * 3600


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


def a_cache_written(cache_path, seconds_ago=0):
    cache_path.write_text("\n".join([ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2]) + "\n", "utf-8")
    written_at = time.time() - seconds_ago
    os.utime(cache_path, (written_at, written_at))


def test_a_recent_cache_is_used_without_asking_celestrak_again(celestrak, cache_path):
    a_cache_written(cache_path)

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert celestrak.requests == []


def test_a_cache_older_than_two_hours_is_refreshed(celestrak, cache_path):
    a_cache_written(cache_path, seconds_ago=THREE_HOURS_S)

    a_catalog(celestrak, cache_path).tracked_satellites()

    assert len(celestrak.requests) == 1
    assert time.time() - cache_path.stat().st_mtime < 60


def test_when_celestrak_fails_the_last_known_catalog_is_used(celestrak, cache_path):
    a_cache_written(cache_path, seconds_ago=THREE_HOURS_S)
    celestrak.fails_with(503)

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544


def test_a_response_that_is_not_a_catalog_never_replaces_the_cache(celestrak, cache_path):
    a_cache_written(cache_path, seconds_ago=THREE_HOURS_S)
    celestrak.publishes("No GP data found")

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert ISS_TLE_LINE_1 in cache_path.read_text("utf-8")


def test_without_cache_nor_celestrak_the_catalog_is_unavailable(celestrak, cache_path):
    celestrak.fails_with(503)

    with pytest.raises(CatalogUnavailableError):
        a_catalog(celestrak, cache_path).tracked_satellites()
