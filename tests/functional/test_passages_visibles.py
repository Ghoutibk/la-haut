from pytest_bdd import given, scenarios, then

from la_haut.interface.http.presenters import present_pass
from tests.support.fixtures import (
    DOCKED_VEHICLE_NAME,
    DOCKED_VEHICLE_TLE_LINE_1,
    DOCKED_VEHICLE_TLE_LINE_2,
)
from tests.support.french import DIRECTIONS, is_about

scenarios("passages_visibles.feature")


@given("un vaisseau amarré à l'ISS dans le catalogue")
def a_docked_vehicle_in_the_catalog(catalog_path):
    entry = [DOCKED_VEHICLE_NAME, DOCKED_VEHICLE_TLE_LINE_1, DOCKED_VEHICLE_TLE_LINE_2]
    with catalog_path.open("a", encoding="utf-8") as catalog:
        catalog.write("\n".join(entry) + "\n")


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
        assert present_pass(visible_pass)["name"] == expected["nom"]
        assert is_about(visible_pass.starts_at, expected["jour"], expected["début"])
        assert is_about(visible_pass.ends_at, expected["jour"], expected["fin"])
        assert visible_pass.appears_in == DIRECTIONS[expected["depuis"]]
        assert visible_pass.vanishes_in == DIRECTIONS[expected["vers"]]
