from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then

from tests.support.visit import NO_GEOLOCATION, REFUSED_POSITION, a_shared_position

scenarios("page/position.feature")


@given(
    parsers.parse(
        "je suis à {city}, en {latitude:g}, {longitude:g}, et que j'accepte de donner ma position"
    )
)
def i_share_my_position(visit, city, latitude, longitude):
    visit.position = a_shared_position(latitude, longitude)


@given("je refuse de donner ma position")
def i_refuse_to_share_my_position(visit):
    visit.position = REFUSED_POSITION


@given("mon navigateur ne sait pas me localiser")
def my_browser_cannot_locate_me(visit):
    visit.position = NO_GEOLOCATION


@then(parsers.parse("l'en-tête indique « {place} »"))
def the_header_shows_the_place(page, place):
    expect(page.get_by_role("banner").get_by_text(place, exact=True)).to_be_visible()


@then("Là-haut n'a encore cherché aucun passage")
def no_pass_was_searched_yet(visible_passes_listing):
    assert visible_passes_listing.requests == []
