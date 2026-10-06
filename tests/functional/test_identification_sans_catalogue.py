import pytest
from pytest_bdd import given, scenarios, then

from la_haut.composition import build_identify_sighting_from_celestrak
from tests.support.fake_celestrak import FakeCelestrak

scenarios("identification_sans_catalogue.feature")


@pytest.fixture
def celestrak():
    with FakeCelestrak() as fake:
        yield fake


@given("Là-haut n'a jamais pu joindre CelesTrak", target_fixture="identify_sighting")
def celestrak_never_reached(celestrak, tmp_path):
    celestrak.fails_with(503)
    return build_identify_sighting_from_celestrak(
        tmp_path / "visual.csv", url_template=celestrak.url_template
    )


@then("les satellites n'ont pas pu être vérifiés")
def the_satellites_could_not_be_checked(identification):
    assert not identification.satellites_checked
