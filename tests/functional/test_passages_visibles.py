from datetime import time, timedelta

from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.composition import build_list_visible_passes
from la_haut.domain.time_window import TimeWindow
from tests.support.fixtures import (
    DOCKED_VEHICLE_NAME,
    DOCKED_VEHICLE_TLE_LINE_1,
    DOCKED_VEHICLE_TLE_LINE_2,
)
from tests.support.french import (
    DIRECTIONS,
    french_date,
    paris_instant,
    paris_instant_from_hour_text,
)

scenarios("passages_visibles.feature")

TOLERANCE = timedelta(minutes=1)


@given("un vaisseau amarré à l'ISS dans le catalogue")
def a_docked_vehicle_in_the_catalog(catalog_path):
    entry = [DOCKED_VEHICLE_NAME, DOCKED_VEHICLE_TLE_LINE_1, DOCKED_VEHICLE_TLE_LINE_2]
    with catalog_path.open("a", encoding="utf-8") as catalog:
        catalog.write("\n".join(entry) + "\n")


@when(
    parsers.parse("je cherche les passages visibles du {start} au {end}"),
    target_fixture="passes",
)
def search_visible_passes(observer, catalog_path, start, end):
    window = TimeWindow(
        starts_at=paris_instant_from_hour_text(start),
        ends_at=paris_instant_from_hour_text(end),
    )
    return build_list_visible_passes(catalog_path).execute(observer, window)


@then("je ne vois aucun passage")
def no_pass_is_announced(passes):
    assert passes == []


@then("le vaisseau amarré est signalé avec l'ISS")
def the_docked_vehicle_travels_with_the_iss(passes):
    [iss_pass] = passes
    assert iss_pass.docked_with == (DOCKED_VEHICLE_NAME,)


@then("je vois ces passages :")
def these_passes_are_announced(passes, datatable):
    header, *rows = datatable
    expected_passes = [dict(zip(header, row, strict=True)) for row in rows]

    assert len(passes) == len(expected_passes)
    for visible_pass, expected in zip(passes, expected_passes, strict=True):
        day = french_date(expected["jour"])
        assert visible_pass.satellite_name == expected["satellite"]
        expected_start = paris_instant(day, time.fromisoformat(expected["début"]))
        expected_end = paris_instant(day, time.fromisoformat(expected["fin"]))
        assert abs(visible_pass.starts_at - expected_start) <= TOLERANCE
        assert abs(visible_pass.ends_at - expected_end) <= TOLERANCE
        assert visible_pass.appears_in == DIRECTIONS[expected["depuis"]]
        assert visible_pass.vanishes_in == DIRECTIONS[expected["vers"]]
