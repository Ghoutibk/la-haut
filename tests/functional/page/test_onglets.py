import re

from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("page/onglets.feature")


@when("je reviens à la page précédente")
def go_back(page):
    page.go_back()


@then(parsers.parse("l'adresse de la page finit par {anchor}"))
def the_address_ends_with(page, anchor):
    expect(page).to_have_url(re.compile(re.escape(anchor) + "$"))
