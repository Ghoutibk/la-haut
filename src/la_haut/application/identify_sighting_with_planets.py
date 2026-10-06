from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.ports import CatalogUnavailableError, PlanetLocator
from la_haut.domain.identification import Identification
from la_haut.domain.observer import Observer
from la_haut.domain.planet import Planet
from la_haut.domain.sighting import Sighting


class IdentifySightingWithPlanets:
    """Cas d'usage décoré : « c'était quoi, ça ? » parmi les satellites, puis les planètes.

    Un satellite qui collait au signalement l'emporte : une lumière qui bouge n'est pas une
    planète. Les planètes viennent ensuite, de la plus proche à la plus éloignée de la direction.
    Sans catalogue de satellites, les planètes répondent quand même, et l'identification le dit.
    """

    def __init__(self, identify_sighting: IdentifySighting, planets: PlanetLocator) -> None:
        self._identify_sighting = identify_sighting
        self._planets = planets

    def execute(self, observer: Observer, sighting: Sighting) -> Identification:
        angles = {
            position: position.angle_to(sighting)
            for position in (
                self._planets.locate(planet, observer, sighting.at) for planet in Planet
            )
        }
        planets = sorted(
            (position for position, angle in angles.items() if angle is not None),
            key=lambda position: angles[position],
        )
        try:
            satellites = self._identify_sighting.execute(observer, sighting)
        except CatalogUnavailableError:
            return Identification(candidates=tuple(planets), satellites_checked=False)
        return Identification(candidates=(*satellites, *planets))
