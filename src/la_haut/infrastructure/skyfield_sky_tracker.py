import math
from datetime import datetime, timedelta
from functools import lru_cache

from skyfield.api import EarthSatellite, wgs84

from la_haut.domain.compass_point import FULL_TURN_DEG
from la_haut.domain.observer import Observer
from la_haut.domain.orbit_mean_elements import OrbitMeanElements
from la_haut.domain.satellite import Satellite
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow
from la_haut.infrastructure.bundled_ephemeris import load_bundled_ephemeris

DEFAULT_STEP = timedelta(seconds=10)


def _instants(window: TimeWindow, step: timedelta) -> list[datetime]:
    count = math.ceil(window.duration / step)
    return [window.starts_at + index * step for index in range(count)]


class SkyfieldSkyTracker:
    """Adaptateur SkyTracker : propagation SGP4 et position du Soleil avec Skyfield, hors ligne."""

    def __init__(self, step: timedelta = DEFAULT_STEP) -> None:
        self._timescale, self._ephemeris = load_bundled_ephemeris()
        self._earth = self._ephemeris["earth"]
        self._sun = self._ephemeris["sun"]
        self._step = step
        # Tous les satellites d'une recherche partagent la fenêtre et l'observateur : la rotation
        # de la Terre (nutation) et la hauteur du Soleil ne se calculent qu'une fois pour eux.
        self._sky_clock = lru_cache(maxsize=8)(self._compute_sky_clock)

    def _compute_sky_clock(self, observer: Observer, window: TimeWindow):
        instants = _instants(window, self._step)
        times = self._timescale.from_datetimes(instants)
        place = wgs84.latlon(
            observer.latitude_deg, observer.longitude_deg, elevation_m=observer.altitude_m
        )
        sun_elevations, _, _ = (self._earth + place).at(times).observe(self._sun).apparent().altaz()
        return instants, times, place, sun_elevations

    def _orbiter(self, satellite: Satellite) -> EarthSatellite:
        elements = satellite.elements
        if isinstance(elements, OrbitMeanElements):
            orbiter = EarthSatellite.from_omm(self._timescale, elements.as_fields())
            orbiter.name = satellite.name
            return orbiter
        return EarthSatellite(elements.line_1, elements.line_2, satellite.name, self._timescale)

    def track(
        self, satellite: Satellite, observer: Observer, window: TimeWindow
    ) -> list[SkySample]:
        instants, times, place, sun_elevations = self._sky_clock(observer, window)
        orbiter = self._orbiter(satellite)

        elevations, azimuths, _ = (orbiter - place).at(times).altaz()
        sunlit = orbiter.at(times).is_sunlit(self._ephemeris)

        return [
            SkySample(
                at=instant,
                azimuth_deg=float(azimuth) % FULL_TURN_DEG,
                elevation_deg=float(elevation),
                is_sunlit=bool(is_lit),
                sun_elevation_deg=float(sun_elevation),
            )
            for instant, azimuth, elevation, is_lit, sun_elevation in zip(
                instants,
                azimuths.degrees,
                elevations.degrees,
                sunlit,
                sun_elevations.degrees,
                strict=True,
            )
        ]
