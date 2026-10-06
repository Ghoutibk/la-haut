from dataclasses import dataclass

from la_haut.domain.planet import PlanetPosition
from la_haut.domain.visible_pass import VisiblePass


@dataclass(frozen=True, slots=True)
class Identification:
    """La réponse à « c'était quoi, ça ? » : les candidats, du plus au moins probable."""

    candidates: tuple[VisiblePass | PlanetPosition, ...]
