"""Ports : ce dont l'application a besoin, sans dire comment c'est fait."""

from datetime import datetime
from typing import Protocol

from la_haut.domain.identification import Identification
from la_haut.domain.observer import Observer
from la_haut.domain.planet import Planet, PlanetPosition
from la_haut.domain.satellite import Satellite
from la_haut.domain.sighting import Sighting
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visible_pass import VisiblePass


class CatalogUnavailableError(RuntimeError):
    """Aucun catalogue de satellites n'est disponible, même ancien."""


class SatelliteCatalog(Protocol):
    def tracked_satellites(self) -> list[Satellite]:
        """Les satellites que Là-haut suit pour ses utilisateurs."""
        ...


class SkyTracker(Protocol):
    def track(
        self, satellite: Satellite, observer: Observer, window: TimeWindow
    ) -> list[SkySample]:
        """La trace chronologique du satellite dans le ciel de l'observateur."""
        ...


class PlanetLocator(Protocol):
    def locate(self, planet: Planet, observer: Observer, at: datetime) -> PlanetPosition:
        """Où se trouve la planète dans le ciel de l'observateur à cet instant."""
        ...


class VisiblePassesListing(Protocol):
    """Ce que l'interface attend de « Ce soir », calculé à chaque fois ou par créneaux."""

    def execute(self, observer: Observer, window: TimeWindow) -> list[VisiblePass]: ...


class SightingIdentification(Protocol):
    """Ce que l'interface attend de « c'était quoi, ça ? », planètes comprises ou non."""

    def execute(self, observer: Observer, sighting: Sighting) -> Identification: ...
