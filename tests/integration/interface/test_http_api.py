from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.observer import Observer
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.app import create_app
from tests.support.builders import DEFAULT_INSTANT, a_satellite, a_track
from tests.support.fakes import FakeSatelliteCatalog, FakeSkyTracker

PARIS = {"latitude": 48.8566, "longitude": 2.3522}


def a_client(tracks_by_name, tracker=None):
    tracker = tracker or FakeSkyTracker(tracks_by_name)
    satellites = [a_satellite(name) for name in tracks_by_name]
    list_visible_passes = ListVisiblePasses(
        catalog=FakeSatelliteCatalog(satellites), tracker=tracker
    )
    app = create_app(
        list_visible_passes, IdentifySighting(list_visible_passes), clock=lambda: DEFAULT_INSTANT
    )
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
