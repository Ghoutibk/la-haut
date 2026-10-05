from dataclasses import dataclass
from datetime import datetime, timedelta

from la_haut.domain.compass_point import CompassPoint

# Une heure donnée de mémoire, à quelques minutes près.
SIGHTING_TIME_TOLERANCE = timedelta(minutes=5)


class InvalidSightingError(ValueError):
    """Un signalement doit dire à quel instant précis la lumière a été vue."""


@dataclass(frozen=True, slots=True)
class Sighting:
    """Ce que raconte un observateur : « j'ai vu une lumière à telle heure, par là »."""

    at: datetime
    direction: CompassPoint

    def __post_init__(self) -> None:
        if self.at.tzinfo is None:
            raise InvalidSightingError("L'instant doit porter un fuseau horaire")
