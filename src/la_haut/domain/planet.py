from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from la_haut.domain.compass_point import FULL_TURN_DEG, CompassPoint
from la_haut.domain.sighting import Sighting
from la_haut.domain.visibility import CIVIL_TWILIGHT_END_SUN_ELEVATION_DEG

HORIZON_ELEVATION_DEG = 0.0


class Planet(StrEnum):
    """Les planètes brillantes que l'on prend pour un satellite ou un avion, des plus brillantes
    en général aux moins brillantes."""

    VENUS = "venus"
    JUPITER = "jupiter"
    MARS = "mars"
    SATURN = "saturn"


@dataclass(frozen=True, slots=True)
class PlanetPosition:
    """Où se trouve une planète dans le ciel de l'observateur à un instant donné."""

    planet: Planet
    at: datetime
    azimuth_deg: float
    elevation_deg: float
    sun_elevation_deg: float

    @property
    def direction(self) -> CompassPoint:
        return CompassPoint.from_azimuth(self.azimuth_deg)

    def angle_to(self, sighting: Sighting) -> float | None:
        """Écart en azimut entre la planète et la direction du signalement.

        None si la planète était sous l'horizon, dans un ciel trop clair, ou ailleurs.
        """
        if (
            self.elevation_deg <= HORIZON_ELEVATION_DEG
            or self.sun_elevation_deg > CIVIL_TWILIGHT_END_SUN_ELEVATION_DEG
            or not self.direction.is_close_to(sighting.direction)
        ):
            return None
        gap = abs(self.azimuth_deg - sighting.direction.azimuth_deg) % FULL_TURN_DEG
        return min(gap, FULL_TURN_DEG - gap)
