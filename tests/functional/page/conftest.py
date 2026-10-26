"""Étapes partagées par les scénarios de la page, pilotée dans le Google Chrome de la machine.

Le site tourne sur un port libre de localhost, branché sur les doublures de `tests/support`.
"""

import os
import re
from dataclasses import replace
from datetime import date, datetime, time, timedelta

import pytest
from playwright.sync_api import expect, sync_playwright
from pytest_bdd import given, parsers, then, when

from la_haut.application.send_feedback import SendFeedback
from la_haut.composition import STATIC_DIR
from la_haut.domain.observer import Observer
from la_haut.domain.sighting import Sighting
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.app import create_app
from tests.support.builders import (
    a_planet_position,
    a_satellite,
    a_visible_pass,
    an_observer_in_paris,
)
from tests.support.fakes import (
    FakeFeedbackInbox,
    FakeSightingIdentification,
    FakeVisiblePassesListing,
)
from tests.support.fixtures import (
    HUBBLE_NAME,
    HUBBLE_TLE_LINE_1,
    HUBBLE_TLE_LINE_2,
    STARLINK_TRAIN,
    TIANGONG_NAME,
    TIANGONG_TLE_LINE_1,
    TIANGONG_TLE_LINE_2,
)
from tests.support.french import DIRECTIONS, PARIS_TIME, PLANETS, french_date, paris_instant
from tests.support.local_site import LocalSite, eventually
from tests.support.visit import (
    UNANSWERED_POSITION,
    Visit,
    a_group,
    a_tab,
    a_view,
    ask_to_identify,
    choose_the_direction,
)

# Un lundi soir d'octobre à Paris : l'heure du visiteur et du site, sauf mention contraire.
MONDAY_EVENING = datetime(2026, 10, 5, 21, 30, tzinfo=PARIS_TIME)
STARLINK_TRAIN_NAME = re.compile(r"train Starlink de (?P<size>\d+) satellites")
API_PATHS = {
    "chercher les passages": "/api/passes",
    "identifier ma lumière": "/api/identification",
    "recevoir mon message": "/api/feedback",
}
# Le numéro NORAD de chaque satellite qu'un scénario peut nommer : c'est par lui que Là-haut
# trouve le nom public d'un satellite célèbre.
NORAD_IDS = {
    satellite.name: satellite.norad_id
    for satellite in (
        a_satellite(),
        a_satellite(TIANGONG_NAME, (TIANGONG_TLE_LINE_1, TIANGONG_TLE_LINE_2)),
        a_satellite(HUBBLE_NAME, (HUBBLE_TLE_LINE_1, HUBBLE_TLE_LINE_2)),
        *(a_satellite(name, (line_1, line_2)) for name, line_1, line_2 in STARLINK_TRAIN),
    )
}


@pytest.fixture(scope="session")
def chrome():
    """Le Google Chrome installé sur la machine, sans fenêtre : un seul pour toute la session.

    Là où Google Chrome ne s'installe pas, `LA_HAUT_BROWSER_EXECUTABLE` désigne un Chromium.
    """
    executable = os.environ.get("LA_HAUT_BROWSER_EXECUTABLE")
    with sync_playwright() as playwright:
        if executable:
            browser = playwright.chromium.launch(executable_path=executable, headless=True)
        else:
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


def a_pass_from(row: dict[str, str], day: date):
    """Un passage décrit par une ligne de scénario ; un train Starlink se nomme par sa taille."""
    starts_at = paris_instant(day, time.fromisoformat(row["début"]))
    ends_at = paris_instant(day, time.fromisoformat(row["fin"]))
    if ends_at < starts_at:
        ends_at += timedelta(days=1)
    names = [row["satellite"]]
    train = STARLINK_TRAIN_NAME.fullmatch(row["satellite"])
    if train:
        names = [name for name, *_ in STARLINK_TRAIN][: int(train["size"])]
    return a_visible_pass(
        satellite_name=names[0],
        norad_id=NORAD_IDS[names[0]],
        train_followers=tuple(names[1:]),
        starts_at=starts_at,
        ends_at=ends_at,
        appears_in=DIRECTIONS[row["depuis"]],
        vanishes_in=DIRECTIONS[row["vers"]],
        max_elevation_deg=float(row["hauteur"]),
    )


def rows_of(datatable) -> list[dict[str, str]]:
    header, *rows = datatable
    return [dict(zip(header, row, strict=True)) for row in rows]


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
            static_dir=STATIC_DIR,
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


@given("je ne réponds pas à la demande de position")
def i_do_not_answer_the_position_request(visit):
    visit.position = UNANSWERED_POSITION


@when(parsers.parse("{seconds:d} secondes passent"))
def seconds_go_by(page, seconds):
    page.clock.run_for(seconds * 1000)


@when(parsers.parse("{minutes:d} minutes passent"))
def minutes_go_by(page, minutes):
    page.clock.run_for(minutes * 60 * 1000)


@then(parsers.parse("la vue « {title} » annonce « {status} »"))
def the_view_announces(page, title, status):
    expect(a_view(page, title).get_by_role("status")).to_have_text(status)


def _passes_were_searched_over(listing, observer, visit, hours):
    def searched():
        assert listing.requests == [
            (observer, TimeWindow(visit.now, visit.now + timedelta(hours=hours)))
        ]

    eventually(searched)


@then(
    parsers.parse(
        "Là-haut cherche les passages des {hours:d} prochaines heures "
        "en {latitude:g}, {longitude:g}"
    )
)
def passes_are_searched_there(visible_passes_listing, visit, hours, latitude, longitude):
    observer = Observer(latitude_deg=latitude, longitude_deg=longitude)
    _passes_were_searched_over(visible_passes_listing, observer, visit, hours)


@then(
    parsers.parse("Là-haut cherche les passages des {hours:d} prochaines heures au-dessus de Paris")
)
def passes_are_searched_over_paris(visible_passes_listing, visit, hours):
    _passes_were_searched_over(visible_passes_listing, an_observer_in_paris(), visit, hours)


@given(parsers.parse("nous sommes le {day} à {clock}"))
def it_is(visit, day, clock):
    visit.now = paris_instant(french_date(day), time.fromisoformat(clock))


@given("Là-haut annonce ces passages :", target_fixture="visible_passes_listing")
def la_haut_announces_these_passes(datatable):
    return FakeVisiblePassesListing(
        [a_pass_from(row, french_date(row["jour"])) for row in rows_of(datatable)]
    )


@given("Là-haut y reconnaît ces passages :")
def la_haut_recognizes_these_passes(sighting_identification, visit, datatable):
    passes = tuple(a_pass_from(row, visit.now.date()) for row in rows_of(datatable))
    identification = sighting_identification.identification
    sighting_identification.identification = replace(
        identification, candidates=identification.candidates + passes
    )


@given("Là-haut y reconnaît ces planètes :")
def la_haut_recognizes_these_planets(sighting_identification, datatable):
    planets = tuple(
        a_planet_position(
            planet=PLANETS[row["planète"]],
            azimuth_deg=DIRECTIONS[row["direction"]].azimuth_deg,
            elevation_deg=float(row["hauteur"]),
        )
        for row in rows_of(datatable)
    )
    identification = sighting_identification.identification
    sighting_identification.identification = replace(
        identification, candidates=identification.candidates + planets
    )


@given("Là-haut n'a pas pu vérifier les satellites")
def la_haut_could_not_check_the_satellites(sighting_identification):
    sighting_identification.identification = replace(
        sighting_identification.identification, satellites_checked=False
    )


@given(parsers.parse("Là-haut met du temps à {action}"))
def la_haut_takes_its_time(site, action):
    site.holds(API_PATHS[action])


@given("l'hébergeur de Là-haut est en panne")
def the_host_is_down(site):
    site.goes_down_on("/api/")


@when("Là-haut répond enfin")
def la_haut_answers_at_last(site):
    site.answers()


@when(parsers.parse("je choisis la direction « {direction} »"))
def i_choose_the_direction(page, direction):
    choose_the_direction(page, direction)


@when("je demande à identifier ma lumière")
def i_ask_to_identify_my_light(page):
    ask_to_identify(page)


@then(parsers.parse("seul « {choice} » est choisi parmi « {legend} »"))
def only_this_choice_is_made(page, choice, legend):
    chosen = a_group(page, legend).get_by_role("button", pressed=True)

    expect(chosen).to_have_count(1)
    expect(chosen).to_have_accessible_name(choice)


@then("aucune direction n'est choisie")
def no_direction_is_chosen(page):
    chosen = a_group(page, "Dans quelle direction ?").get_by_role("button", pressed=True)
    expect(chosen).to_have_count(0)


@then(parsers.parse("la vue « {title} » m'alerte : « {message} »"))
def the_view_alerts(page, title, message):
    expect(a_view(page, title).get_by_role("alert")).to_have_text(message)


@then(parsers.parse("la vue « {title} » ne m'alerte plus"))
def the_view_no_longer_alerts(page, title):
    alerts = a_view(page, title).get_by_role("alert").filter(has_text=re.compile(r"\S"))
    expect(alerts).to_have_count(0)


@when(parsers.parse("je touche « {name} »"))
def i_touch_the_button(page, name):
    page.get_by_role("button", name=name, exact=True).click()


@then(parsers.parse("je vois le bouton « {name} »"))
def the_button_is_shown(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).to_be_visible()


@then(parsers.parse("je ne vois pas le bouton « {name} »"))
def the_button_is_not_shown(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).to_be_hidden()


@then(parsers.parse("la page dit « {text} »"))
def the_page_says(page, text):
    expect(page.get_by_text(text, exact=True)).to_be_visible()


@then(parsers.parse("la page ne dit pas « {text} »"))
def the_page_does_not_say(page, text):
    expect(page.get_by_text(text, exact=True)).to_be_hidden()


@then(parsers.parse("le bouton « {name} » indique qu'il travaille"))
def the_button_is_busy(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).to_have_attribute("aria-busy", "true")


@then(parsers.parse("le bouton « {name} » ne travaille plus"))
def the_button_is_no_longer_busy(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).not_to_have_attribute(
        "aria-busy", "true"
    )


@then(
    parsers.re(
        r"Là-haut cherche ce qui était (?:au |à l')(?P<direction>[a-z-]+) "
        r"le (?P<day>.+) à (?P<clock>[\d:]+), au-dessus de Paris"
    )
)
def la_haut_searches_what_was_there(sighting_identification, direction, day, clock):
    sighting = Sighting(
        at=paris_instant(french_date(day), time.fromisoformat(clock)),
        direction=DIRECTIONS[direction],
    )

    def searched():
        assert sighting_identification.requests == [(an_observer_in_paris(), sighting)]

    eventually(searched)


@then(parsers.parse("la réponse « {title} » est annoncée sans m'interrompre"))
def the_answer_is_announced_politely(page, title):
    """Le titre de la réponse est dans une région vivante, lue quand le lecteur d'écran se tait."""
    live_region = page.get_by_role("heading", name=title, exact=True).locator(
        "xpath=ancestor::*[@aria-live][1]"
    )
    expect(live_region).to_have_attribute("aria-live", "polite")
