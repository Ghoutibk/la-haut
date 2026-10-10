from dataclasses import dataclass

from la_haut.domain.planet import PlanetPosition
from la_haut.domain.visible_pass import VisiblePass

# Ce que propose « c'était quoi, ça ? » : un passage (satellite ou train Starlink) ou une planète.
Candidate = VisiblePass | PlanetPosition


@dataclass(frozen=True, slots=True)
class Identification:
    """La réponse à « c'était quoi, ça ? » : les candidats, du plus au moins probable."""

    candidates: tuple[Candidate, ...]
    # Faux quand le catalogue des satellites manquait : seules les planètes ont été cherchées.
    satellites_checked: bool = True
