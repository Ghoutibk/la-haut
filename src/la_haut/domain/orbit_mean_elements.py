import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime

# Les champs OMM dont la propagation SGP4 a besoin, tels que CelesTrak les publie.
TEXT_FIELDS = ("OBJECT_ID", "CLASSIFICATION_TYPE")
EPOCH_FIELD = "EPOCH"
EPOCH_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DECIMAL_FIELDS = (
    "MEAN_MOTION",
    "ECCENTRICITY",
    "INCLINATION",
    "RA_OF_ASC_NODE",
    "ARG_OF_PERICENTER",
    "MEAN_ANOMALY",
    "BSTAR",
    "MEAN_MOTION_DOT",
    "MEAN_MOTION_DDOT",
)
INTEGER_FIELDS = ("NORAD_CAT_ID", "EPHEMERIS_TYPE", "ELEMENT_SET_NO", "REV_AT_EPOCH")
ELEMENT_FIELDS = (*TEXT_FIELDS, EPOCH_FIELD, *DECIMAL_FIELDS, *INTEGER_FIELDS)
# Désignation internationale : année sur quatre chiffres, numéro du lancement, lettres de la pièce.
INTERNATIONAL_DESIGNATOR = re.compile(r"\d{2}(?P<year>\d{2})-(?P<number>\d{3})[A-Z]+")


class InvalidOrbitMeanElementsError(ValueError):
    """Des éléments orbitaux incomplets ou illisibles donneraient des positions fausses."""


def _check_field(name: str, value: str) -> None:
    try:
        if name in INTEGER_FIELDS:
            int(value)
        elif name in DECIMAL_FIELDS:
            float(value)
        elif name == EPOCH_FIELD:
            datetime.strptime(value, EPOCH_FORMAT)
    except ValueError as error:
        raise InvalidOrbitMeanElementsError(f"Champ OMM {name} illisible : {value!r}") from error


@dataclass(frozen=True, slots=True)
class OrbitMeanElements:
    """Les éléments orbitaux moyens d'un satellite, au format OMM du CCSDS publié par CelesTrak.

    À la différence du TLE, ils acceptent les numéros NORAD au-delà de 99999, donnés depuis
    mi-2026 aux objets nouvellement lancés. Les valeurs restent telles que publiées.
    """

    fields: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        names = {name for name, _ in self.fields}
        missing = [name for name in ELEMENT_FIELDS if name not in names]
        if missing:
            raise InvalidOrbitMeanElementsError(f"Champs OMM manquants : {', '.join(missing)}")
        for name, value in self.fields:
            _check_field(name, value)

    @classmethod
    def from_fields(cls, fields: Mapping[str, str]) -> "OrbitMeanElements":
        """Garde, d'un message OMM, les seuls éléments orbitaux."""
        return cls(tuple((name, fields[name]) for name in ELEMENT_FIELDS if name in fields))

    def as_fields(self) -> dict[str, str]:
        return dict(self.fields)

    @property
    def norad_id(self) -> int:
        return int(self.as_fields()["NORAD_CAT_ID"])

    @property
    def launch(self) -> str:
        """Le lancement, écrit comme dans un TLE : l'année sur deux chiffres et le numéro."""
        match = INTERNATIONAL_DESIGNATOR.fullmatch(self.as_fields()["OBJECT_ID"])
        return f"{match['year']}{match['number']}" if match else ""
