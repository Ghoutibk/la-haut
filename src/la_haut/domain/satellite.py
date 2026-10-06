from dataclasses import dataclass

from la_haut.domain.orbit_mean_elements import OrbitMeanElements

TLE_LINE_LENGTH = 69
CHECKSUM_INDEX = 68
CATALOG_NUMBER = slice(2, 7)
# Désignation internationale (colonnes 10 à 17) sans la lettre de la pièce : année et numéro.
LAUNCH = slice(9, 14)


class InvalidTwoLineElementsError(ValueError):
    """Des éléments orbitaux corrompus donneraient des positions fausses."""


def _checksum(line: str) -> int:
    """Somme des chiffres, chaque signe moins compte pour 1, modulo 10."""
    total = sum(int(char) if char.isdigit() else char == "-" for char in line[:CHECKSUM_INDEX])
    return total % 10


def _check_line(line: str, line_number: int) -> None:
    if len(line) != TLE_LINE_LENGTH or not line.startswith(f"{line_number} "):
        raise InvalidTwoLineElementsError(f"Ligne {line_number} mal formée : {line!r}")
    if _checksum(line) != int(line[CHECKSUM_INDEX]):
        raise InvalidTwoLineElementsError(f"Somme de contrôle fausse en ligne {line_number}")


@dataclass(frozen=True, slots=True)
class TwoLineElements:
    """Les éléments orbitaux d'un satellite, au format TLE publié par le NORAD."""

    line_1: str
    line_2: str

    def __post_init__(self) -> None:
        _check_line(self.line_1, line_number=1)
        _check_line(self.line_2, line_number=2)
        if self.line_1[CATALOG_NUMBER] != self.line_2[CATALOG_NUMBER]:
            raise InvalidTwoLineElementsError("Les deux lignes décrivent des satellites différents")

    @property
    def norad_id(self) -> int:
        return int(self.line_1[CATALOG_NUMBER])

    @property
    def launch(self) -> str:
        """Le lancement qui a mis l'objet en orbite, commun à toutes ses pièces."""
        return self.line_1[LAUNCH]


@dataclass(frozen=True, slots=True)
class Satellite:
    """Un objet en orbite que l'on peut suivre dans le ciel, connu par ses TLE ou son OMM."""

    name: str
    elements: TwoLineElements | OrbitMeanElements

    @property
    def norad_id(self) -> int:
        return self.elements.norad_id
