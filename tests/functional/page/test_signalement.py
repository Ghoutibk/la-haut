import re
from datetime import time

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.sighting import Sighting
from tests.support.builders import an_observer_in_paris
from tests.support.fakes import FakeSkyTracker, UnavailableSatelliteCatalog
from tests.support.french import DIRECTIONS, french_date, paris_instant
from tests.support.local_site import eventually
from tests.support.visit import a_group, a_view

scenarios("page/signalement.feature")

SIGHTING_VIEW = "Tu as vu une lumière bouger dans le ciel ?"
COMPASS_CELL = re.compile(r"(?P<text>\S+) \((?P<name>[^)]+)\)")
# Au pixel près : les cases d'une même ligne ou d'une même colonne sont alignées.
ALIGNMENT_PX = 1


@given(
    "Là-haut ne cherche que parmi les satellites, dont le catalogue est indisponible",
    target_fixture="sighting_identification",
)
def la_haut_only_searches_unavailable_satellites():
    return IdentifySighting(
        ListVisiblePasses(catalog=UnavailableSatelliteCatalog(), tracker=FakeSkyTracker({}))
    )


@when(parsers.parse("je dis l'avoir vue « {moment} »"))
def i_say_when_i_saw_it(page, moment):
    a_group(page, "Quand ?").get_by_role("button", name=moment, exact=True).click()


@when(parsers.parse("j'indique l'heure {local_time}"))
def i_give_the_time(page, local_time):
    page.get_by_label("Heure à laquelle tu l'as vue").fill(local_time)


@then(parsers.parse("je vois le champ « {label} »"))
def the_field_is_shown(page, label):
    expect(page.get_by_label(label)).to_be_visible()


@then(parsers.parse("je ne vois pas le champ « {label} »"))
def the_field_is_not_shown(page, label):
    expect(page.get_by_label(label)).to_be_hidden()


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


@then("Là-haut n'a rien cherché")
def la_haut_searched_nothing(sighting_identification):
    assert sighting_identification.requests == []


def _compass_cell(page, cell):
    view = a_view(page, SIGHTING_VIEW)
    button = COMPASS_CELL.fullmatch(cell)
    if button is None:
        return view.get_by_text(cell, exact=True)
    found = view.get_by_role("button", name=button["name"], exact=True)
    expect(found).to_have_text(button["text"])
    return found


def _center(box):
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


@then("la rose des vents propose, ligne par ligne :")
def the_compass_rose_offers(page, datatable):
    _, *rows = datatable
    centers = [[_center(_compass_cell(page, cell).bounding_box()) for cell in row] for row in rows]

    for row in centers:
        assert all(abs(y - row[0][1]) <= ALIGNMENT_PX for _, y in row)
        assert [x for x, _ in row] == sorted(x for x, _ in row)
    for column in zip(*centers, strict=True):
        assert all(abs(x - column[0][0]) <= ALIGNMENT_PX for x, _ in column)
        assert [y for _, y in column] == sorted(y for _, y in column)


@then("aucune direction n'est choisie")
def no_direction_is_chosen(page):
    chosen = a_group(page, "Dans quelle direction ?").get_by_role("button", pressed=True)
    expect(chosen).to_have_count(0)


@then(parsers.parse("la page rappelle « {reminder} »"))
def the_page_reminds(page, reminder):
    expect(page.get_by_text(reminder, exact=True)).to_be_visible()


@then(parsers.parse("le bouton « {name} » indique qu'il travaille"))
def the_button_is_busy(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).to_have_attribute("aria-busy", "true")


@then(parsers.parse("le bouton « {name} » ne travaille plus"))
def the_button_is_no_longer_busy(page, name):
    expect(page.get_by_role("button", name=name, exact=True)).not_to_have_attribute(
        "aria-busy", "true"
    )
