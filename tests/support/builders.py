"""Builders de données de test : un seul endroit pour les valeurs par défaut (DRY)."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from la_haut.domain.sky_sample import SkySample

DEFAULT_INSTANT = datetime(2026, 10, 5, 19, 42, tzinfo=UTC)
ONE_MINUTE = timedelta(minutes=1)


def a_sky_sample(**overrides) -> SkySample:
    """Un échantillon visible à l'œil nu par défaut ; chaque test ne change que ce qui compte."""
    sample = SkySample(
        at=DEFAULT_INSTANT,
        azimuth_deg=270.0,
        elevation_deg=45.0,
        is_sunlit=True,
        sun_elevation_deg=-12.0,
    )
    return replace(sample, **overrides)


def a_track(*samples_overrides: dict, start: datetime = DEFAULT_INSTANT) -> list[SkySample]:
    """Une suite d'échantillons espacés d'une minute, à partir de `start`."""
    return [
        a_sky_sample(at=start + index * ONE_MINUTE, **overrides)
        for index, overrides in enumerate(samples_overrides)
    ]
