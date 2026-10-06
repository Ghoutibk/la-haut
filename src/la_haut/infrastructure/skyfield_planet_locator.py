from datetime import datetime

from skyfield.api import wgs84

from la_haut.domain.compass_point import FULL_TURN_DEG
from la_haut.domain.observer import Observer
from la_haut.domain.planet import Planet, PlanetPosition
from la_haut.infrastructure.bundled_ephemeris import load_bundled_ephemeris

# DE421 donne Vénus et Mars elles-mêmes, Jupiter et Saturne par le barycentre de leur système.
EPHEMERIS_TARGETS = {
    Planet.VENUS: "venus",
    Planet.MARS: "mars",
    Planet.JUPITER: "jupiter barycenter",
    Planet.SATURN: "saturn barycenter",
}


class SkyfieldPlanetLocator:
    """Adaptateur PlanetLocator : positions apparentes avec Skyfield et DE421, hors ligne."""

    def __init__(self) -> None:
        self._timescale, self._ephemeris = load_bundled_ephemeris()

    def locate(self, planet: Planet, observer: Observer, at: datetime) -> PlanetPosition:
        time = self._timescale.from_datetime(at)
        place = self._ephemeris["earth"] + wgs84.latlon(
            observer.latitude_deg, observer.longitude_deg, elevation_m=observer.altitude_m
        )
        sky = place.at(time)
        elevation, azimuth, _ = (
            sky.observe(self._ephemeris[EPHEMERIS_TARGETS[planet]]).apparent().altaz()
        )
        sun_elevation, _, _ = sky.observe(self._ephemeris["sun"]).apparent().altaz()
        return PlanetPosition(
            planet=planet,
            at=at,
            azimuth_deg=float(azimuth.degrees) % FULL_TURN_DEG,
            elevation_deg=float(elevation.degrees),
            sun_elevation_deg=float(sun_elevation.degrees),
        )
