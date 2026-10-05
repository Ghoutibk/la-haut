from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.identify_sighting_with_planets import IdentifySightingWithPlanets
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.ports import CatalogUnavailableError
from la_haut.domain.observer import Observer
from la_haut.domain.planet import Planet
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.app import create_app
from tests.support.builders import (
    DEFAULT_INSTANT,
    ONE_MINUTE,
    a_planet_position,
    a_satellite,
    a_track,
)
from tests.support.fakes import FakePlanetLocator, FakeSatelliteCatalog, FakeSkyTracker

PARIS = {"latitude": 48.8566, "longitude": 2.3522}
WEST = {"azimuth_deg": 270.0}


def a_client(tracks_by_name, tracker=None, planets=()):
    tracker = tracker or FakeSkyTracker(tracks_by_name)
    satellites = [a_satellite(name) for name in tracks_by_name]
    list_visible_passes = ListVisiblePasses(
        catalog=FakeSatelliteCatalog(satellites), tracker=tracker
    )
    identify_sighting = IdentifySightingWithPlanets(
        IdentifySighting(list_visible_passes), FakePlanetLocator(list(planets))
    )
    app = create_app(list_visible_passes, identify_sighting, clock=lambda: DEFAULT_INSTANT)
    return TestClient(app)


def test_tonight_lists_the_visible_passes_over_the_observer():
    response = a_client({"ISS (ZARYA)": a_track({}, {}, {})}).get("/api/passes", params=PARIS)

    assert response.status_code == 200
    [iss_pass] = response.json()["passes"]
    assert (iss_pass["satellite"], iss_pass["starts_at"]) == (
        "ISS (ZARYA)",
        DEFAULT_INSTANT.isoformat(),
    )


def test_tonight_searches_the_next_twelve_hours_by_default():
    tracker = FakeSkyTracker({})

    a_client({"ISS (ZARYA)": []}, tracker=tracker).get("/api/passes", params=PARIS)

    [(_, observer, window)] = tracker.requests
    assert observer == Observer(latitude_deg=48.8566, longitude_deg=2.3522)
    assert window == TimeWindow(DEFAULT_INSTANT, DEFAULT_INSTANT + timedelta(hours=12))


@pytest.mark.parametrize(
    "params",
    [
        {**PARIS, "hours": 0},
        {**PARIS, "hours": 49},
        {"latitude": 91, "longitude": 2.3522},
        {"latitude": 48.8566},
    ],
)
def test_tonight_rejects_an_impossible_request(params):
    response = a_client({}).get("/api/passes", params=params)

    assert response.status_code == 422


def test_a_sighting_is_identified_over_http():
    seen = {**PARIS, "at": (DEFAULT_INSTANT + ONE_MINUTE).isoformat(), "direction": "W"}

    response = a_client({"ISS (ZARYA)": a_track(WEST, WEST, WEST)}).get(
        "/api/identification", params=seen
    )

    assert response.status_code == 200
    [candidate] = response.json()["candidates"]
    assert candidate["satellite"] == "ISS (ZARYA)"


def test_each_candidate_says_whether_it_is_a_satellite_or_a_planet():
    seen = {**PARIS, "at": (DEFAULT_INSTANT + ONE_MINUTE).isoformat(), "direction": "W"}
    venus = a_planet_position(planet=Planet.VENUS, azimuth_deg=270.0)

    response = a_client({"ISS (ZARYA)": a_track(WEST, WEST, WEST)}, planets=[venus]).get(
        "/api/identification", params=seen
    )

    satellite, planet = response.json()["candidates"]
    assert satellite["kind"] == "satellite"
    assert (planet["kind"], planet["name"]) == ("planet", "Vénus")


def test_a_sighting_matching_no_satellite_gives_no_candidate():
    seen = {**PARIS, "at": DEFAULT_INSTANT.isoformat(), "direction": "N"}

    response = a_client({"ISS (ZARYA)": a_track(WEST, WEST)}).get(
        "/api/identification", params=seen
    )

    assert response.json() == {"candidates": []}


@pytest.mark.parametrize(
    "seen",
    [
        {**PARIS, "at": "2026-10-05T21:42:00", "direction": "W"},
        {**PARIS, "at": DEFAULT_INSTANT.isoformat(), "direction": "WEST"},
        {**PARIS, "direction": "W"},
    ],
)
def test_an_incomplete_or_ambiguous_sighting_is_rejected(seen):
    response = a_client({}).get("/api/identification", params=seen)

    assert response.status_code == 422


class UnavailableCatalog:
    def tracked_satellites(self):
        raise CatalogUnavailableError("CelesTrak injoignable et aucun cache")


def test_the_api_says_so_when_no_catalog_is_available():
    list_visible_passes = ListVisiblePasses(
        catalog=UnavailableCatalog(), tracker=FakeSkyTracker({})
    )
    client = TestClient(create_app(list_visible_passes, IdentifySighting(list_visible_passes)))

    response = client.get("/api/passes", params=PARIS)

    assert response.status_code == 503
    assert "catalogue" in response.json()["detail"]


def test_the_web_page_is_served_at_the_root():
    response = a_client({}).get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Là-haut" in response.text


@pytest.mark.parametrize("asset", ["/static/app.js", "/static/style.css"])
def test_the_page_assets_are_served(asset):
    assert a_client({}).get(asset).status_code == 200
