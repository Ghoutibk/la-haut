"""Doublures des ports de l'application, pour tester sans Skyfield ni réseau."""

from datetime import datetime

from la_haut.application.ports import CatalogUnavailableError
from la_haut.domain.observer import Observer
from la_haut.domain.planet import Planet, PlanetPosition
from la_haut.domain.satellite import Satellite
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow


class FakeSatelliteCatalog:
    def __init__(self, satellites: list[Satellite]) -> None:
        self._satellites = satellites

    def tracked_satellites(self) -> list[Satellite]:
        return list(self._satellites)


class FakeSkyTracker:
    """Renvoie une trace préparée par nom de satellite et retient chaque demande."""

    def __init__(self, tracks_by_name: dict[str, list[SkySample]]) -> None:
        self._tracks_by_name = tracks_by_name
        self.requests: list[tuple[str, Observer, TimeWindow]] = []

    def track(
        self, satellite: Satellite, observer: Observer, window: TimeWindow
    ) -> list[SkySample]:
        self.requests.append((satellite.name, observer, window))
        return self._tracks_by_name.get(satellite.name, [])


class UnavailableSatelliteCatalog:
    """Un catalogue injoignable et sans cache."""

    def tracked_satellites(self) -> list[Satellite]:
        raise CatalogUnavailableError("CelesTrak injoignable et aucun cache")


class FakePlanetLocator:
    """La position préparée de chaque planète (sous l'horizon sinon) ; retient les demandes."""

    def __init__(self, positions: list[PlanetPosition]) -> None:
        self._positions = {position.planet: position for position in positions}
        self.requests: list[tuple[Planet, Observer, datetime]] = []

    def locate(self, planet: Planet, observer: Observer, at: datetime) -> PlanetPosition:
        self.requests.append((planet, observer, at))
        below_the_horizon = PlanetPosition(planet, at, 0.0, -30.0, -30.0)
        return self._positions.get(planet, below_the_horizon)
