import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.application.send_feedback import SendFeedback
from la_haut.domain.feedback import FeedbackKind
from tests.support.fakes import UnavailableFeedbackInbox
from tests.support.local_site import eventually

scenarios("page/fenetre_d_avis.feature")

FEEDBACK_WINDOW = "Un souci, une idée ?"
MESSAGE = "Ton message"
CONTACT = "Ton e-mail, si tu veux une réponse (facultatif)"
KINDS = {
    "un problème": FeedbackKind.PROBLEM,
    "une idée": FeedbackKind.IDEA,
    "autre chose": FeedbackKind.OTHER,
}


def _window(page):
    return page.get_by_role("dialog", name=FEEDBACK_WINDOW, exact=True)


def _header_button(page, name):
    return page.get_by_role("banner").get_by_role("button", name=name, exact=True)


@given("la boîte à avis est prête")
def the_feedback_inbox_is_ready():
    """La boîte à avis par défaut reçoit tout ce qui lui est remis."""


@given(
    "Là-haut a déjà reçu trop de messages cette heure-ci",
    target_fixture="send_feedback",
)
def too_many_messages_this_hour(feedback_inbox):
    return SendFeedback(feedback_inbox, max_per_hour=0)


@given("la boîte à avis est injoignable", target_fixture="send_feedback")
def the_feedback_inbox_is_unreachable():
    return SendFeedback(UnavailableFeedbackInbox())


@when(parsers.parse("je touche « {name} » dans l'en-tête"))
def i_touch_in_the_header(page, name):
    _header_button(page, name).click()


@when("j'ouvre la fenêtre d'avis", target_fixture="page")
def i_open_the_feedback_window(opens):
    page = opens("/")
    _header_button(page, "Avis").click()
    return page


@when(parsers.parse("je change l'adresse pour {anchor}"))
def i_change_the_address(page, anchor):
    page.evaluate("anchor => { location.hash = anchor; }", anchor)


@when(parsers.parse("je choisis « {choice} » parmi « {legend} »"))
def i_choose_among(page, choice, legend):
    group = _window(page).get_by_role("group", name=legend, exact=True)
    group.get_by_role("button", name=choice, exact=True).click()


@when(parsers.parse("j'écris « {message} »"))
def i_write(page, message):
    _window(page).get_by_label(MESSAGE).fill(message)


@when(parsers.parse("j'écris un message de {length:d} caractères"))
def i_write_a_message_of(page, length):
    _window(page).get_by_label(MESSAGE).fill("x" * length)


@when(parsers.parse("je laisse mon e-mail {contact}"))
def i_leave_my_email(page, contact):
    _window(page).get_by_label(CONTACT).fill(contact)


@when(parsers.parse("je laisse une adresse de {length:d} caractères"))
def i_leave_an_address_of(page, length):
    domain = "@example.org"
    _window(page).get_by_label(CONTACT).fill("x" * (length - len(domain)) + domain)


@when("j'envoie mon message")
def i_send_my_message(page):
    _window(page).get_by_role("button", name="Envoyer", exact=True).click()


@when("j'appuie sur Échap")
def i_press_escape(page):
    page.keyboard.press("Escape")


@when("je touche le fond assombri, hors de la fenêtre")
def i_touch_the_backdrop(page):
    box = _window(page).bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] / 2)


@when("je touche la fenêtre, hors de ses boutons et de ses champs")
def i_touch_the_window_itself(page):
    box = _window(page).bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + 4)


@when(parsers.parse("je valide au clavier depuis le champ « {label} »"))
def i_submit_with_the_keyboard(page, label):
    _window(page).get_by_label(label).press("Enter")


@when(parsers.parse("un robot remplit le champ « {label} » avec « {value} »"))
def a_robot_fills_the_field(page, label, value):
    page.get_by_label(label).fill(value, force=True)


@then(parsers.parse("la fenêtre « {title} » est ouverte"))
def the_window_is_open(page, title):
    expect(page.get_by_role("dialog", name=title, exact=True)).to_be_visible()


@then(parsers.parse("la fenêtre « {title} » est fermée"))
def the_window_is_closed(page, title):
    expect(page.get_by_role("dialog", name=title, exact=True)).to_be_hidden()


@then(parsers.parse("la fenêtre dit « {text} »"))
def the_window_says(page, text):
    expect(_window(page).get_by_text(text, exact=True)).to_be_visible()


@then(parsers.parse("la fenêtre ne dit pas « {text} »"))
def the_window_does_not_say(page, text):
    expect(_window(page).get_by_text(text, exact=True)).to_be_hidden()


@then(parsers.parse("la fenêtre s'intitule désormais « {title} »"))
def the_window_now_reads(page, title):
    expect(_window(page).get_by_role("heading", name=title, exact=True)).to_be_visible()


@then(parsers.parse("la fenêtre m'alerte : « {message} »"))
def the_window_alerts(page, message):
    expect(_window(page).get_by_role("alert")).to_have_text(message)


@then("la fenêtre ne m'alerte plus")
def the_window_no_longer_alerts(page):
    alerts = _window(page).get_by_role("alert").filter(has_text=re.compile(r"\S"))
    expect(alerts).to_have_count(0)


@then(parsers.parse("le champ « {label} » est vide"))
def the_field_is_empty(page, label):
    expect(_window(page).get_by_label(label)).to_have_value("")


@then(parsers.parse("le champ « {label} » contient « {value} »"))
def the_field_holds(page, label, value):
    expect(_window(page).get_by_label(label)).to_have_value(value)


@then(parsers.parse("le champ « {label} » garde {length:d} caractères"))
def the_field_keeps(page, label, length):
    assert len(_window(page).get_by_label(label).input_value()) == length


@then(parsers.parse("l'auteur reçoit {kind} : « {message} », avec l'e-mail {contact}"))
def the_author_receives_with_contact(feedback_inbox, kind, message, contact):
    _the_author_receives(feedback_inbox, (KINDS[kind], message, contact))


@then(parsers.parse("l'auteur reçoit {kind} : « {message} », sans e-mail"))
def the_author_receives_without_contact(feedback_inbox, kind, message):
    _the_author_receives(feedback_inbox, (KINDS[kind], message, None))


def _the_author_receives(inbox, expected):
    def received():
        assert [(f.kind, f.message, f.contact) for f, _ in inbox.delivered] == [expected]

    eventually(received)


@then("l'auteur ne reçoit rien")
def the_author_receives_nothing(feedback_inbox):
    assert feedback_inbox.delivered == []


@then(parsers.parse("le champ « {label} » est hors de l'écran et caché aux lecteurs d'écran"))
def the_field_is_out_of_sight(page, label):
    expect(page.get_by_label(label)).not_to_be_in_viewport()
    expect(page.get_by_role("textbox", name=label)).to_have_count(0)


@then(parsers.parse("le clavier passe du champ « {field} » au bouton « {button} »"))
def the_keyboard_goes_from_to(page, field, button):
    window = _window(page)
    window.get_by_label(field).focus()
    page.keyboard.press("Tab")
    expect(window.get_by_role("button", name=button, exact=True)).to_be_focused()
