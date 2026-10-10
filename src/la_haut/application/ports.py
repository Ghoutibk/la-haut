"""Ports : ce dont l'application a besoin, sans dire comment c'est fait."""

from datetime import datetime
from typing import Protocol

from la_haut.domain.feedback import Feedback
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


class FeedbackUnavailableError(RuntimeError):
    """La boîte à avis est injoignable ou pas encore configurée."""


class FeedbackNotConfiguredError(FeedbackUnavailableError):
    """Aucun dépôt ni jeton n'est réglé : les avis ne partent nulle part."""


class SatelliteCatalog(Protocol):
    def tracked_satellites(self) -> list[Satellite]:
        """Les satellites que Là-haut suit pour ses utilisateurs."""
        ...


class SkyTracker(Protocol):
    def track(
        self, satellite: Satellite, observer: Observer, window: TimeWindow
    ) -> list[SkySample]:
        """La trace chronologique du satellite dans le ciel de l'observateur.

        Elle peut omettre les moments où il est sous l'horizon : chaque passage reste alors bordé
        d'un instant sous l'horizon, pour que deux passages ne se touchent jamais.
        """
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


class FeedbackInbox(Protocol):
    def deliver(self, feedback: Feedback, sent_at: datetime) -> None:
        """Remet l'avis d'un visiteur à l'auteur du site."""
        ...
