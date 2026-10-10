import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then

from la_haut.application.list_visible_passes import ListVisiblePasses
from tests.support.fakes import FakeSkyTracker, UnavailableSatelliteCatalog
from tests.support.visit import a_view

scenarios("page/ce_soir.feature")

TONIGHT = "Au-dessus de toi"
WEEKDAYS = re.compile("lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche")


def _pass_cards(page):
    return a_view(page, TONIGHT).get_by_role("listitem")


@given("le catalogue des satellites est indisponible", target_fixture="visible_passes_listing")
def the_satellite_catalog_is_unavailable():
    return ListVisiblePasses(catalog=UnavailableSatelliteCatalog(), tracker=FakeSkyTracker({}))


@then("je vois ces passages :")
def these_passes_are_shown(page, datatable):
    header, *rows = datatable
    cards = _pass_cards(page)

    expect(cards).to_have_count(len(rows))
    for index, row in enumerate(rows):
        card = cards.nth(index)
        expected = dict(zip(header, row, strict=True))
        for column in ("heure", "nom", "chemin", "hauteur"):
            expect(card).to_contain_text(expected[column])
        if expected["jour"]:
            expect(card).to_contain_text(expected["jour"])
        else:
            expect(card).not_to_contain_text(WEEKDAYS)


@then(parsers.parse("le passage « {name} » explique « {explanation} »"))
def the_pass_explains(page, name, explanation):
    expect(_pass_cards(page).filter(has_text=name)).to_contain_text(explanation)


@then("je ne vois aucun passage")
def no_pass_is_shown(page):
    expect(_pass_cards(page)).to_have_count(0)
