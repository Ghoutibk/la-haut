from pytest_bdd import scenarios, then

scenarios("identification_sans_catalogue.feature")


@then("les satellites n'ont pas pu être vérifiés")
def the_satellites_could_not_be_checked(identification):
    assert not identification.satellites_checked
