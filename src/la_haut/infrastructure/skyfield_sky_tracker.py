import math
from datetime import datetime, timedelta
from functools import lru_cache
from typing import NamedTuple

import numpy as np
from skyfield.api import EarthSatellite, wgs84
from skyfield.nutationlib import iau2000a_radians
from skyfield.timelib import Time
from skyfield.toposlib import GeographicPosition

from la_haut.domain.compass_point import FULL_TURN_DEG
from la_haut.domain.observer import Observer
from la_haut.domain.orbit_mean_elements import OrbitMeanElements
from la_haut.domain.satellite import Satellite
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow
from la_haut.infrastructure.bundled_ephemeris import load_bundled_ephemeris

DEFAULT_STEP = timedelta(seconds=10)
# Un satellite qui monte à 10° reste plusieurs minutes au-dessus de l'horizon : un balayage toutes
# les minutes trouve tous ses passages, que l'on échantillonne ensuite au pas fin.
SCAN_STEP = timedelta(minutes=1)
HORIZON_DEG = 0.0


def _instants(window: TimeWindow, step: timedelta) -> list[datetime]:
    count = math.ceil(window.duration / step)
    return [window.starts_at + index * step for index in range(count)]


def _around_the_passes(scan: np.ndarray, is_up: np.ndarray, count: int) -> np.ndarray:
    """Les instants fins entre le balayage qui précède et celui qui suit chaque balayage où le
    satellite est au-dessus de l'horizon : chaque passage reste bordé d'instants sous l'horizon."""
    selected = np.zeros(count, dtype=bool)
    for index in np.flatnonzero(is_up):
        first = scan[max(index - 1, 0)]
        last = scan[min(index + 1, len(scan) - 1)]
        selected[first : last + 1] = True
    return np.flatnonzero(selected)


class _SkyClock(NamedTuple):
    """Ce que partagent tous les satellites d'une recherche : mêmes instants, même observateur."""

    instants: list[datetime]
    times: Time
    nutation_radians: tuple[np.ndarray, np.ndarray]
    place: GeographicPosition
    scan: np.ndarray
    scan_times: Time
    sun_elevations_deg: np.ndarray

    def times_at(self, indices: np.ndarray) -> Time:
        """Ces instants de la fenêtre, avec la nutation déjà calculée pour toute la fenêtre.

        Skyfield ne recopie pas ses calculs en cache quand on découpe un Time : sans cela, la
        nutation (IAU 2000A, le gros du calcul) serait refaite pour chaque satellite. Si Skyfield
        renomme ce cache, le résultat reste juste ; seul le temps de calcul remonte.
        """
        times = self.times[indices]
        psi, epsilon = self.nutation_radians
        times._nutation_angles_radians = (psi[indices], epsilon[indices])
        return times


class SkyfieldSkyTracker:
    """Adaptateur SkyTracker : propagation SGP4 et position du Soleil avec Skyfield, hors ligne.

    La trace ne couvre que les moments où le satellite est au-dessus de l'horizon, au pas fin,
    bordés d'un instant sous l'horizon : rien n'est calculé entre ses passages.
    """

    def __init__(self, step: timedelta = DEFAULT_STEP) -> None:
        self._timescale, self._ephemeris = load_bundled_ephemeris()
        self._earth = self._ephemeris["earth"]
        self._sun = self._ephemeris["sun"]
        self._step = step
        # Tous les satellites d'une recherche partagent la fenêtre et l'observateur : la rotation
        # de la Terre (nutation) et la hauteur du Soleil ne se calculent qu'une fois pour eux.
        self._sky_clock = lru_cache(maxsize=8)(self._compute_sky_clock)

    def _compute_sky_clock(self, observer: Observer, window: TimeWindow) -> _SkyClock:
        instants = _instants(window, self._step)
        times = self._timescale.from_datetimes(instants)
        place = wgs84.latlon(
            observer.latitude_deg, observer.longitude_deg, elevation_m=observer.altitude_m
        )
        every = max(1, round(SCAN_STEP / self._step))
        scan = np.unique(np.append(np.arange(0, len(instants), every), len(instants) - 1))
        clock = _SkyClock(instants, times, iau2000a_radians(times), place, scan, None, None)
        scan_times = clock.times_at(scan)
        sun_on_scan, _, _ = (
            (self._earth + place).at(scan_times).observe(self._sun).apparent().altaz()
        )
        # Le Soleil monte ou descend lentement : entre deux balayages, l'interpolation linéaire
        # s'écarte de moins d'une seconde d'arc du calcul complet.
        sun_elevations_deg = np.interp(np.arange(len(instants)), scan, sun_on_scan.degrees)
        return clock._replace(scan_times=scan_times, sun_elevations_deg=sun_elevations_deg)

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
        clock = self._sky_clock(observer, window)
        orbiter = self._orbiter(satellite)

        scanned_elevations, _, _ = (orbiter - clock.place).at(clock.scan_times).altaz()
        selected = _around_the_passes(
            clock.scan, scanned_elevations.degrees > HORIZON_DEG, len(clock.instants)
        )
        if not len(selected):
            return []

        times = clock.times_at(selected)
        elevations, azimuths, _ = (orbiter - clock.place).at(times).altaz()
        sunlit = orbiter.at(times).is_sunlit(self._ephemeris)

        return [
            SkySample(
                at=clock.instants[index],
                azimuth_deg=float(azimuth) % FULL_TURN_DEG,
                elevation_deg=float(elevation),
                is_sunlit=bool(is_lit),
                sun_elevation_deg=float(clock.sun_elevations_deg[index]),
            )
            for index, azimuth, elevation, is_lit in zip(
                selected, azimuths.degrees, elevations.degrees, sunlit, strict=True
            )
        ]
