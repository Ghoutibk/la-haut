from dataclasses import dataclass

from la_haut.domain.sky_sample import SkySample

MIN_NAKED_EYE_ELEVATION_DEG = 10.0
CIVIL_TWILIGHT_END_SUN_ELEVATION_DEG = -6.0


@dataclass(frozen=True, slots=True)
class NakedEyeVisibility:
    """Visible à l'œil nu : éclairé par le Soleil, assez haut, dans un ciel assez sombre."""

    min_elevation_deg: float = MIN_NAKED_EYE_ELEVATION_DEG
    max_sun_elevation_deg: float = CIVIL_TWILIGHT_END_SUN_ELEVATION_DEG

    def allows(self, sample: SkySample) -> bool:
        return (
            sample.is_sunlit
            and sample.elevation_deg >= self.min_elevation_deg
            and sample.sun_elevation_deg <= self.max_sun_elevation_deg
        )
