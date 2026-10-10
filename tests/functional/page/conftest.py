"""Étapes partagées par les scénarios de la page, pilotée dans le Google Chrome de la machine.

Le site tourne sur un port libre de localhost, branché sur les doublures de `tests/support`.
"""

from datetime import datetime

import pytest
from playwright.sync_api import expect, sync_playwright
from pytest_bdd import parsers, then, when

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
MAIN_NAVIGATION = "Navigation principale"


def a_view(page, title: str):
    """Une vue de la page, nommée par son titre."""
    return page.get_by_role("region", name=title, exact=True)


def a_tab(page, name: str):
    return page.get_by_role("navigation", name=MAIN_NAVIGATION).get_by_role(
        "link", name=name, exact=True
    )


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


@when(parsers.parse("je touche l'onglet « {tab} »"))
def touch_a_tab(page, tab):
    a_tab(page, tab).click()


@then(parsers.parse("je vois la vue « {title} »"))
def the_view_is_shown(page, title):
    expect(a_view(page, title)).to_be_visible()


@then(parsers.parse("la vue « {title} » est cachée"))
def the_view_is_hidden(page, title):
    expect(a_view(page, title)).to_be_hidden()


@then(parsers.parse("l'onglet « {tab} » est l'onglet actif"))
def the_tab_is_the_current_one(page, tab):
    expect(a_tab(page, tab)).to_have_attribute("aria-current", "page")


@then(parsers.parse("l'onglet « {tab} » ne l'est pas"))
def the_tab_is_not_the_current_one(page, tab):
    expect(a_tab(page, tab)).not_to_have_attribute("aria-current", "page")
