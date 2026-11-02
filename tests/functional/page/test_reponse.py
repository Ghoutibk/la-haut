from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

from tests.support.local_site import eventually
from tests.support.visit import (
    MAIN_NAVIGATION,
    SIGHTING_VIEW,
    a_view,
    an_answer,
    ask_to_identify,
    choose_the_direction,
)

scenarios("page/reponse.feature")


@when(
    parsers.parse("je signale une lumière vue à l'instant, direction « {direction} »"),
    target_fixture="page",
)
def i_report_a_light_seen_just_now(opens, direction):
    page = opens("/#cetait-quoi")
    choose_the_direction(page, direction)
    ask_to_identify(page)
    return page


@then(parsers.parse("la réponse est « {answer} », sous « {eyebrow} »"))
def the_answer_is(page, answer, eyebrow):
    view = a_view(page, SIGHTING_VIEW)
    expect(view.get_by_role("heading", name=answer, exact=True)).to_be_visible()
    expect(view.get_by_text(eyebrow, exact=True)).to_be_visible()


@then(parsers.parse("la réponse dit « {sentence} »"))
def the_answer_says(page, sentence):
    expect(a_view(page, SIGHTING_VIEW).get_by_text(sentence, exact=True)).to_be_visible()


@then(parsers.parse("la réponse propose « {action} »"))
def the_answer_offers(page, action):
    view = a_view(page, SIGHTING_VIEW)
    expect(view.get_by_role("button", name=action, exact=True)).to_be_visible()


@then(parsers.parse("je vois toute la réponse « {title} », au-dessus des onglets"))
def the_whole_answer_is_on_screen(page, title):
    """La carte tient entre le haut de l'écran et la barre des onglets, sans défiler à la main."""
    card = an_answer(page, title)
    tabs = page.get_by_role("navigation", name=MAIN_NAVIGATION)
    expect(card).to_be_visible()

    def on_screen():
        box = card.bounding_box()
        tabs_top = tabs.bounding_box()["y"]
        assert box["y"] >= 0, f"la carte commence à {box['y']:.0f} px, au-dessus de l'écran"
        bottom = box["y"] + box["height"]
        assert bottom <= tabs_top, (
            f"la carte finit à {bottom:.0f} px, sous les onglets qui commencent à {tabs_top:.0f} px"
        )

    eventually(on_screen)
