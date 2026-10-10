"""Étapes partagées par les scénarios de la page, pilotée dans le Google Chrome de la machine.

Le site tourne sur un port libre de localhost, branché sur les doublures de `tests/support`.
"""

from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright
from pytest_bdd import parsers, when

from la_haut.application.send_feedback import SendFeedback
from la_haut.interface.http.app import create_app
from tests.support.fakes import (
    FakeFeedbackInbox,
    FakeSightingIdentification,
    FakeVisiblePassesListing,
)
from tests.support.french import PARIS_TIME
from tests.support.local_site import LocalSite
from tests.support.visit import Visit

# Un lundi soir d'octobre à Paris : l'heure du visiteur et du site, sauf mention contraire.
MONDAY_EVENING = datetime(2026, 10, 5, 21, 30, tzinfo=PARIS_TIME)


@pytest.fixture(scope="session")
def chrome():
    """Le Google Chrome installé sur la machine, sans fenêtre : un seul pour toute la session."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def local_site():
    with LocalSite() as site:
        yield site


@pytest.fixture
def site(local_site):
    yield local_site
    local_site.reset()


@pytest.fixture
def visit(chrome, site):
    visit = Visit(chrome, site.url, now=MONDAY_EVENING)
    yield visit
    visit.ends()


@pytest.fixture
def visible_passes_listing():
    """Par défaut, aucun passage ce soir."""
    return FakeVisiblePassesListing([])


@pytest.fixture
def sighting_identification():
    """Par défaut, rien de connu dans le ciel."""
    return FakeSightingIdentification()


@pytest.fixture
def feedback_inbox():
    return FakeFeedbackInbox()


@pytest.fixture
def send_feedback(feedback_inbox):
    return SendFeedback(feedback_inbox)


@pytest.fixture
def opens(visit, site, visible_passes_listing, sighting_identification, send_feedback):
    """Ouvre une adresse de Là-haut, servi par les doublures réglées jusque-là."""

    def open_address(path: str):
        app = create_app(
            visible_passes_listing,
            sighting_identification,
            clock=lambda: visit.now,
            send_feedback=send_feedback,
        )
        site.serves(app)
        return visit.opens(path)

    return open_address


@when("j'ouvre Là-haut", target_fixture="page")
def open_la_haut(opens):
    return opens("/")


@when(parsers.parse("j'ouvre l'adresse {address}"), target_fixture="page")
def open_an_address(opens, address):
    return opens("/" + address)
