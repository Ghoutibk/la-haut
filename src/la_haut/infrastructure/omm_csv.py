import csv
import io

from la_haut.domain.orbit_mean_elements import OrbitMeanElements
from la_haut.domain.satellite import Satellite

NAME_FIELD = "OBJECT_NAME"


class InvalidOmmCatalogError(ValueError):
    """Un texte qui ne se lit pas comme un catalogue OMM : une page web, par exemple."""


def parse_omm_csv(text: str) -> list[Satellite]:
    """Lit un catalogue OMM au format CSV de CelesTrak : un satellite par ligne, après l'en-tête."""
    try:
        return [_satellite_from(row) for row in csv.DictReader(io.StringIO(text))]
    except csv.Error as error:
        raise InvalidOmmCatalogError(f"Texte illisible en CSV : {error}") from error


def _satellite_from(row: dict[str, str]) -> Satellite:
    name = row.get(NAME_FIELD)
    if name is None:
        raise InvalidOmmCatalogError(f"Ligne sans {NAME_FIELD} : ce n'est pas un catalogue OMM")
    return Satellite(name=name.strip(), elements=OrbitMeanElements.from_fields(row))
