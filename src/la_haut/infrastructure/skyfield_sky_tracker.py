import math
from datetime import datetime, timedelta

from skyfield.api import EarthSatellite, Loader, wgs84
from skyfield_data import get_skyfield_data_path

from la_haut.domain.compass_point import FULL_TURN_DEG
from la_haut.domain.observer import Observer
from la_haut.domain.satellite import Satellite
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow

DEFAULT_STEP = timedelta(seconds=10)
EPHEMERIS_FILE = "de421.bsp"


def _instants(window: TimeWindow, step: timedelta) -> list[datetime]:
    count = math.ceil(window.duration / step)
    return [window.starts_at + index * step for index in range(count)]


class SkyfieldSkyTracker:
    """Adaptateur SkyTracker : propagation SGP4 et position du Soleil avec Skyfield, hors ligne."""

    def __init__(self, step: timedelta = DEFAULT_STEP) -> None:
        load = Loader(get_skyfield_data_path(), verbose=False)
        self._timescale = load.timescale(builtin=True)
        self._ephemeris = load(EPHEMERIS_FILE)
        self._earth = self._ephemeris["earth"]
        self._sun = self._ephemeris["sun"]
        self._step = step

    def track(
        self, satellite: Satellite, observer: Observer, window: TimeWindow
    ) -> list[SkySample]:
        instants = _instants(window, self._step)
        times = self._timescale.from_datetimes(instants)
        orbiter = EarthSatellite(
            satellite.elements.line_1, satellite.elements.line_2, satellite.name, self._timescale
        )
        place = wgs84.latlon(
            observer.latitude_deg, observer.longitude_deg, elevation_m=observer.altitude_m
        )

        elevations, azimuths, _ = (orbiter - place).at(times).altaz()
        sunlit = orbiter.at(times).is_sunlit(self._ephemeris)
        sun_elevations, _, _ = (self._earth + place).at(times).observe(self._sun).apparent().altaz()

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
