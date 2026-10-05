"""Ports : ce dont l'application a besoin, sans dire comment c'est fait."""

from typing import Protocol

from la_haut.domain.observer import Observer
from la_haut.domain.satellite import Satellite
from la_haut.domain.sky_sample import SkySample
from la_haut.domain.time_window import TimeWindow


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
