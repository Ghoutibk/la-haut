"""Étapes Gherkin partagées par toutes les fonctionnalités."""

from datetime import time

import pytest
from pytest_bdd import given, parsers, then, when

from la_haut.composition import build_identify_sighting, build_list_visible_passes
from la_haut.domain.sighting import Sighting
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import an_observer_in_paris
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2
from tests.support.french import (
    DIRECTIONS,
    PLANETS,
    french_date,
    paris_instant,
    paris_instant_from_hour_text,
)


@given("un observateur à Paris", target_fixture="observer")
def observer():
    return an_observer_in_paris()


@given(
    "un catalogue qui suit l'ISS avec ses éléments orbitaux du 3 juillet 2018",
    target_fixture="catalog_path",
)
def catalog_path(tmp_path):
    path = tmp_path / "stations.tle"
    path.write_text("\n".join([ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2]) + "\n", "utf-8")
    return path


@pytest.fixture
def list_visible_passes(catalog_path):
    """Par défaut, parmi les satellites du catalogue local."""
    return build_list_visible_passes(catalog_path)


@pytest.fixture
def identify_sighting(catalog_path):
    """Par défaut, parmi les satellites du catalogue local et les planètes."""
    return build_identify_sighting(catalog_path)


@when(
    parsers.parse("je cherche les passages visibles du {start} au {end}"),
    target_fixture="passes",
)
def search_visible_passes(observer, list_visible_passes, start, end):
    window = TimeWindow(
        starts_at=paris_instant_from_hour_text(start),
        ends_at=paris_instant_from_hour_text(end),
    )
    return list_visible_passes.execute(observer, window)


@when(
    parsers.parse("j'ai vu une lumière le {day} à {clock}, direction {direction}"),
    target_fixture="identification",
)
def report_a_sighting(observer, identify_sighting, day, clock, direction):
    sighting = Sighting(
        at=paris_instant(french_date(day), time.fromisoformat(clock)),
        direction=DIRECTIONS[direction],
    )
    return identify_sighting.execute(observer, sighting)


@then(parsers.parse("la lumière était la planète {planet_name}"))
def it_was_the_planet(identification, planet_name):
    assert getattr(identification.candidates[0], "planet", None) == PLANETS[planet_name]
