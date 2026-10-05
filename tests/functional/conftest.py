"""Étapes Gherkin partagées par toutes les fonctionnalités."""

from pytest_bdd import given

from tests.support.builders import an_observer_in_paris
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2


@given("un observateur à Paris", target_fixture="observer")
def observer():
    return an_observer_in_paris()


@given(
    "un catalogue qui suit l'ISS avec ses éléments orbitaux du 3 juillet 2018",
    target_fixture="catalog_path",
)
def catalog_path(tmp_path):
    path = tmp_path / "stations.tle"
    path.write_text("\n".join([ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2]) + "\n", "utf-8")
    return path
