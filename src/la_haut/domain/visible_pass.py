from dataclasses import dataclass
from datetime import datetime, timedelta

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.sighting import SIGHTING_TIME_TOLERANCE, Sighting
from la_haut.domain.sky_sample import SkySample


@dataclass(frozen=True, slots=True)
class VisiblePass:
    """Un moment où un satellite se voit à l'œil nu, de son apparition à sa disparition."""

    satellite_name: str
    starts_at: datetime
    ends_at: datetime
    appears_in: CompassPoint
    vanishes_in: CompassPoint
    max_elevation_deg: float
    docked_with: tuple[str, ...] = ()
    path: tuple[SkySample, ...] = ()
    launch: str = ""

    @property
    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at

    def gap_to(self, sighting: Sighting) -> timedelta | None:
        """Écart entre le signalement et le moment où le passage était dans cette direction.

        None si le passage n'y était pas, ou trop longtemps avant ou après.
        """
        gaps = [
            abs(sample.at - sighting.at)
            for sample in self.path
            if sample.direction.is_close_to(sighting.direction)
        ]
        closest = min(gaps, default=None)
        if closest is None or closest > SIGHTING_TIME_TOLERANCE:
            return None
        return closest
