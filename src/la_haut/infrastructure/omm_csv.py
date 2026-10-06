import csv
import io

from la_haut.domain.orbit_mean_elements import OrbitMeanElements
from la_haut.domain.satellite import Satellite


def parse_omm_csv(text: str) -> list[Satellite]:
    """Lit un catalogue OMM au format CSV de CelesTrak : un satellite par ligne, après l'en-tête."""
    return [
        Satellite(name=row["OBJECT_NAME"].strip(), elements=OrbitMeanElements.from_fields(row))
        for row in csv.DictReader(io.StringIO(text))
    ]
