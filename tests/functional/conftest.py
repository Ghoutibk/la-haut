"""Étapes Gherkin partagées par toutes les fonctionnalités."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, then, when

from la_haut.composition import (
    build_identify_sighting,
    build_identify_sighting_from_celestrak,
    build_list_visible_passes,
    build_list_visible_passes_from_celestrak,
)
from la_haut.domain.sighting import Sighting
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.app import create_app
from tests.support.builders import an_observer_in_paris
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import (
    ISS_NAME,
    ISS_TLE_LINE_1,
    ISS_TLE_LINE_2,
    LAST_30_DAYS_CSV_2026,
    VISUAL_CSV_2026,
)
from tests.support.french import (
    DIRECTIONS,
    PLANETS,
    is_about,
    paris_instant_from_hour_text,
    paris_instant_on,
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
def celestrak():
    with FakeCelestrak() as fake:
        yield fake


@pytest.fixture
def cache_path(tmp_path):
    """Le cache du groupe « visual » ; ceux des autres groupes se rangent à côté."""
    return tmp_path / "visual.csv"


@given("Là-haut n'a jamais pu joindre CelesTrak", target_fixture="identify_sighting")
def celestrak_never_reached(celestrak, cache_path):
    celestrak.fails_with(503)
    return build_identify_sighting_from_celestrak(cache_path, url_template=celestrak.url_template)


@given(
    "CelesTrak publie ses catalogues du 6 octobre 2026 au format OMM",
    target_fixture="list_visible_passes",
)
def celestrak_publishes_its_catalogs_of_october_6(celestrak, cache_path):
    celestrak.publishes(*VISUAL_CSV_2026.splitlines(), group="visual")
    celestrak.publishes(*LAST_30_DAYS_CSV_2026.splitlines(), group="last-30-days")
    return build_list_visible_passes_from_celestrak(cache_path, url_template=celestrak.url_template)


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
        at=paris_instant_on(day, clock),
        direction=DIRECTIONS[direction],
    )
    return identify_sighting.execute(observer, sighting)


@then(parsers.parse("la lumière était la planète {planet_name}"))
def it_was_the_planet(identification, planet_name):
    assert getattr(identification.candidates[0], "planet", None) == PLANETS[planet_name]


@when(parsers.parse("j'ouvre « Ce soir » le {moment}"), target_fixture="tonight")
def open_tonight(observer, celestrak, cache_path, moment, static_dir):
    """La page « Ce soir » du site branché sur CelesTrak, telle qu'elle s'ouvre à ce moment-là."""
    site = create_app(
        build_list_visible_passes_from_celestrak(cache_path, url_template=celestrak.url_template),
        build_identify_sighting_from_celestrak(cache_path, url_template=celestrak.url_template),
        clock=lambda: paris_instant_from_hour_text(moment),
        static_dir=static_dir,
    )
    where = {"latitude": observer.latitude_deg, "longitude": observer.longitude_deg}
    return TestClient(site).get("/api/passes", params=where)


@then(parsers.parse("« Ce soir » annonce « {name} » le {day} de {start} à {end}"))
def tonight_announces(tonight, name, day, start, end):
    assert any(
        announced["name"] == name
        and is_about(datetime.fromisoformat(announced["starts_at"]), day, start)
        and is_about(datetime.fromisoformat(announced["ends_at"]), day, end)
        for announced in tonight.json()["passes"]
    )
