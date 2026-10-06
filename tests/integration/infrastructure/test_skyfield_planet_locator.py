from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from la_haut.domain.planet import Planet
from la_haut.infrastructure.skyfield_planet_locator import SkyfieldPlanetLocator
from tests.support.builders import an_observer_in_paris

PARIS_TIME = ZoneInfo("Europe/Paris")
# Valeurs de référence calculées par un script qui appelle Skyfield directement (DE421,
# position apparente depuis Paris), sans passer par nos adaptateurs.
DUSK = datetime(2018, 7, 3, 22, 45, tzinfo=PARIS_TIME)
DEEP_NIGHT = datetime(2018, 7, 4, 1, 0, tzinfo=PARIS_TIME)
REFERENCE_POSITIONS = [
    # (planète, instant, azimut, hauteur, hauteur du Soleil)
    (Planet.VENUS, DUSK, 279.98, 11.88, -6.70),
    (Planet.SATURN, DEEP_NIGHT, 173.61, 18.42, -17.21),
    (Planet.JUPITER, DEEP_NIGHT, 227.60, 13.49, -17.21),
    (Planet.MARS, DEEP_NIGHT, 140.16, 8.26, -17.21),
]
TOLERANCE_DEG = 0.05


@pytest.fixture(scope="module")
def locator():
    return SkyfieldPlanetLocator()


@pytest.mark.parametrize(("planet", "at", "azimuth", "elevation", "sun"), REFERENCE_POSITIONS)
def test_a_planet_is_located_in_the_sky_of_paris(locator, planet, at, azimuth, elevation, sun):
    position = locator.locate(planet, an_observer_in_paris(), at)

    assert (position.planet, position.at) == (planet, at)
    assert position.azimuth_deg == pytest.approx(azimuth, abs=TOLERANCE_DEG)
    assert position.elevation_deg == pytest.approx(elevation, abs=TOLERANCE_DEG)
    assert position.sun_elevation_deg == pytest.approx(sun, abs=TOLERANCE_DEG)
