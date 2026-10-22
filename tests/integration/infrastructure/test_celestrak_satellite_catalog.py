import logging
import time
from datetime import timedelta

import pytest

from la_haut.application.ports import CatalogUnavailableError
from la_haut.infrastructure.celestrak_satellite_catalog import (
    CELESTRAK_URL_TEMPLATE,
    CelestrakSatelliteCatalog,
)
from tests.support.cache import THREE_HOURS_S, a_cache_written
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2
from tests.support.omm import omm_csv_from_tle

ISS = (ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2)
ISS_CATALOG = omm_csv_from_tle(ISS)

# Chaque façon dont la source des catalogues peut échouer, et la cause qu'en gardent les logs.
SOURCE_FAILURES = {
    "error 503": (lambda celestrak: celestrak.fails_with(503), "503"),
    "web page": (lambda celestrak: celestrak.publishes_a_web_page(), "OBJECT_NAME"),
    "endless line": (lambda celestrak: celestrak.publishes_an_endless_line(), "field limit"),
    "catalog cut short": (
        lambda celestrak: celestrak.publishes_cut_short(ISS_CATALOG),
        "MEAN_ANOMALY",
    ),
    "answer cut off": (lambda celestrak: celestrak.cuts_off_its_answers(), "IncompleteRead"),
}


@pytest.fixture
def celestrak():
    with FakeCelestrak() as fake:
        fake.publishes_as_omm(ISS)
        yield fake


@pytest.fixture(params=list(SOURCE_FAILURES.values()), ids=list(SOURCE_FAILURES))
def celestrak_failure(celestrak, request):
    """CelesTrak échoue d'une des façons possibles ; rend la cause attendue dans les logs."""
    make_it_fail, logged_cause = request.param
    make_it_fail(celestrak)
    return logged_cause


@pytest.fixture
def cache_path(tmp_path):
    return tmp_path / "visual.csv"


def a_catalog(celestrak, cache_path):
    return CelestrakSatelliteCatalog(cache_path, url_template=celestrak.url_template)


def test_celestrak_is_asked_for_the_group_in_omm_csv_format():
    assert CELESTRAK_URL_TEMPLATE.format(group="last-30-days") == (
        "https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=csv"
    )


def test_without_a_cache_the_brightest_satellites_group_is_downloaded(celestrak, cache_path):
    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert celestrak.requests == [{"GROUP": ["visual"], "FORMAT": ["csv"]}]
    assert cache_path.exists()


def test_a_recent_cache_is_used_without_asking_celestrak_again(celestrak, cache_path):
    a_cache_written(cache_path, ISS_CATALOG)

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert celestrak.requests == []


def test_a_cache_older_than_two_hours_is_refreshed(celestrak, cache_path):
    a_cache_written(cache_path, ISS_CATALOG, seconds_ago=THREE_HOURS_S)

    a_catalog(celestrak, cache_path).tracked_satellites()

    assert len(celestrak.requests) == 1
    assert time.time() - cache_path.stat().st_mtime < 60


@pytest.mark.usefixtures("celestrak_failure")
def test_when_celestrak_fails_the_last_known_catalog_is_used(celestrak, cache_path):
    a_cache_written(cache_path, ISS_CATALOG, seconds_ago=THREE_HOURS_S)

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544


def test_a_response_that_is_not_a_catalog_never_replaces_the_cache(celestrak, cache_path):
    a_cache_written(cache_path, ISS_CATALOG, seconds_ago=THREE_HOURS_S)
    celestrak.publishes("No GP data found")

    [iss] = a_catalog(celestrak, cache_path).tracked_satellites()

    assert iss.norad_id == 25544
    assert cache_path.read_bytes() == ISS_CATALOG.encode("utf-8")


@pytest.mark.usefixtures("celestrak_failure")
def test_without_cache_nor_celestrak_the_catalog_is_unavailable(celestrak, cache_path):
    with pytest.raises(CatalogUnavailableError):
        a_catalog(celestrak, cache_path).tracked_satellites()


@pytest.mark.usefixtures("celestrak_failure")
def test_after_a_failure_celestrak_is_left_alone_until_the_retry_delay(celestrak, cache_path):
    catalog = a_catalog(celestrak, cache_path)

    for _ in range(2):
        with pytest.raises(CatalogUnavailableError):
            catalog.tracked_satellites()

    assert len(celestrak.requests) == 1


@pytest.mark.usefixtures("celestrak_failure")
def test_after_a_failure_the_last_known_catalog_answers_without_asking_again(celestrak, cache_path):
    a_cache_written(cache_path, ISS_CATALOG, seconds_ago=THREE_HOURS_S)
    catalog = a_catalog(celestrak, cache_path)

    catalog.tracked_satellites()
    [iss] = catalog.tracked_satellites()

    assert iss.norad_id == 25544
    assert len(celestrak.requests) == 1


@pytest.mark.usefixtures("celestrak_failure")
def test_once_the_retry_delay_is_over_celestrak_is_asked_again(celestrak, cache_path):
    catalog = CelestrakSatelliteCatalog(
        cache_path, url_template=celestrak.url_template, retry_delay=timedelta(0)
    )
    with pytest.raises(CatalogUnavailableError):
        catalog.tracked_satellites()
    celestrak.publishes_as_omm(ISS)

    [iss] = catalog.tracked_satellites()

    assert iss.norad_id == 25544
    assert len(celestrak.requests) == 2


def test_a_failed_download_is_logged_with_its_group_and_its_reason(
    celestrak, celestrak_failure, cache_path, caplog
):
    with caplog.at_level(logging.WARNING), pytest.raises(CatalogUnavailableError):
        a_catalog(celestrak, cache_path).tracked_satellites()

    [record] = caplog.records
    assert record.levelno == logging.WARNING
    assert "visual" in record.getMessage()
    assert celestrak_failure in record.getMessage()
