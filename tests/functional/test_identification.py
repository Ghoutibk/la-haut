from pytest_bdd import parsers, scenarios, then

from tests.support.french import PLANETS

scenarios("identification.feature")


@then(parsers.parse("c'était {satellite_name}"))
def it_was(identification, satellite_name):
    assert identification.candidates[0].satellite_name == satellite_name


@then("ce n'était aucun satellite connu")
def it_was_no_known_satellite(identification):
    assert identification.candidates == ()


@then(parsers.parse("la lumière était la planète {planet_name}"))
def it_was_the_planet(identification, planet_name):
    assert getattr(identification.candidates[0], "planet", None) == PLANETS[planet_name]


@then(parsers.parse("sinon, c'était la planète {planet_name}"))
def otherwise_it_was_the_planet(identification, planet_name):
    assert getattr(identification.candidates[1], "planet", None) == PLANETS[planet_name]
