from datetime import time

from pytest_bdd import parsers, scenarios, then, when

from la_haut.composition import build_identify_sighting
from la_haut.domain.sighting import Sighting
from tests.support.french import DIRECTIONS, french_date, paris_instant

scenarios("identification.feature")


@when(
    parsers.parse("j'ai vu une lumière le {day} à {clock}, direction {direction}"),
    target_fixture="candidates",
)
def report_a_sighting(observer, catalog_path, day, clock, direction):
    sighting = Sighting(
        at=paris_instant(french_date(day), time.fromisoformat(clock)),
        direction=DIRECTIONS[direction],
    )
    return build_identify_sighting(catalog_path).execute(observer, sighting)


@then(parsers.parse("c'était {satellite_name}"))
def it_was(candidates, satellite_name):
    assert candidates[0].satellite_name == satellite_name


@then("ce n'était aucun satellite connu")
def it_was_no_known_satellite(candidates):
    assert candidates == []
