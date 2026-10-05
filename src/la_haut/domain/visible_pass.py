from dataclasses import dataclass
from datetime import datetime, timedelta

from la_haut.domain.compass_point import CompassPoint


@dataclass(frozen=True, slots=True)
class VisiblePass:
    """Un moment où un satellite se voit à l'œil nu, de son apparition à sa disparition."""

    satellite_name: str
    starts_at: datetime
    ends_at: datetime
    appears_in: CompassPoint
    vanishes_in: CompassPoint
    max_elevation_deg: float

    @property
    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at
