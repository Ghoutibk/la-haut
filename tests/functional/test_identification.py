from pytest_bdd import parsers, scenarios, then

scenarios("identification.feature")


@then(parsers.parse("c'était {satellite_name}"))
def it_was(candidates, satellite_name):
    assert candidates[0].satellite_name == satellite_name


@then("ce n'était aucun satellite connu")
def it_was_no_known_satellite(candidates):
    assert candidates == []
