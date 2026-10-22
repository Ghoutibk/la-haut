from pytest_bdd import parsers, scenarios, then

from la_haut.interface.http.presenters import present_candidate
from tests.support.french import PLANETS

scenarios("identification.feature")


@then(parsers.parse("c'était la {public_name}"))
def it_was(identification, public_name):
    assert present_candidate(identification.candidates[0])["name"] == public_name


@then("ce n'était aucun satellite connu")
def it_was_no_known_satellite(identification):
    assert identification.candidates == ()


@then(parsers.parse("sinon, c'était la planète {planet_name}"))
def otherwise_it_was_the_planet(identification, planet_name):
    assert getattr(identification.candidates[1], "planet", None) == PLANETS[planet_name]
