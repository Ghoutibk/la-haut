from datetime import time, timedelta

import pytest
from pytest_bdd import given, parsers, scenarios, then

from la_haut.composition import build_list_visible_passes_from_celestrak
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import LAST_30_DAYS_CSV_2026, VISUAL_CSV_2026
from tests.support.french import french_date, paris_instant

scenarios("trains_starlink_reels.feature")

TOLERANCE = timedelta(minutes=1)


@pytest.fixture
def celestrak():
    with FakeCelestrak() as fake:
        yield fake


@given(
    "CelesTrak publie ses catalogues du 6 octobre 2026 au format OMM",
    target_fixture="list_visible_passes",
)
def celestrak_publishes_its_catalogs_of_october_6(celestrak, tmp_path):
    celestrak.publishes(*VISUAL_CSV_2026.splitlines(), group="visual")
    celestrak.publishes(*LAST_30_DAYS_CSV_2026.splitlines(), group="last-30-days")
    return build_list_visible_passes_from_celestrak(
        tmp_path / "visual.csv", url_template=celestrak.url_template
    )


@then(
    parsers.parse("je vois un train Starlink de {size:d} satellites, le {day} de {start} à {end}")
)
def a_train_among_the_passes(passes, size, day, start, end):
    expected_start = paris_instant(french_date(day), time.fromisoformat(start))
    expected_end = paris_instant(french_date(day), time.fromisoformat(end))
    assert any(
        visible_pass.train_size == size
        and abs(visible_pass.starts_at - expected_start) <= TOLERANCE
        and abs(visible_pass.ends_at - expected_end) <= TOLERANCE
        for visible_pass in passes
    )
