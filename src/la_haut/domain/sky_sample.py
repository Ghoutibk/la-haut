from dataclasses import dataclass
from datetime import datetime

from la_haut.domain.compass_point import CompassPoint

MAX_ABS_ELEVATION_DEG = 90.0


class InvalidSkySampleError(ValueError):
    """Un échantillon de ciel incohérent ne doit jamais entrer dans le domaine."""


@dataclass(frozen=True, slots=True)
class SkySample:
    """Où se trouve un satellite dans le ciel de l'observateur à un instant donné."""

    at: datetime
    azimuth_deg: float
    elevation_deg: float
    is_sunlit: bool
    sun_elevation_deg: float

    def __post_init__(self) -> None:
        if self.at.tzinfo is None:
            raise InvalidSkySampleError("L'instant doit porter un fuseau horaire")
        if abs(self.elevation_deg) > MAX_ABS_ELEVATION_DEG:
            raise InvalidSkySampleError(f"Élévation hors de [-90, 90] : {self.elevation_deg}")
        CompassPoint.from_azimuth(self.azimuth_deg)

    @property
    def direction(self) -> CompassPoint:
        return CompassPoint.from_azimuth(self.azimuth_deg)
