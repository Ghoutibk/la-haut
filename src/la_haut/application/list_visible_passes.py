from la_haut.application.ports import SatelliteCatalog, SkyTracker
from la_haut.domain.docked_passes import merge_docked_passes
from la_haut.domain.observer import Observer
from la_haut.domain.pass_detection import detect_visible_passes
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visibility import NakedEyeVisibility
from la_haut.domain.visible_pass import VisiblePass


class ListVisiblePasses:
    """Cas d'usage : quels satellites verrai-je passer pendant cette fenêtre ?"""

    def __init__(
        self,
        catalog: SatelliteCatalog,
        tracker: SkyTracker,
        visibility: NakedEyeVisibility | None = None,
    ) -> None:
        self._catalog = catalog
        self._tracker = tracker
        self._visibility = visibility or NakedEyeVisibility()

    def execute(self, observer: Observer, window: TimeWindow) -> list[VisiblePass]:
        passes = [
            visible_pass
            for satellite in self._catalog.tracked_satellites()
            for visible_pass in detect_visible_passes(
                satellite.name,
                self._tracker.track(satellite, observer, window),
                self._visibility,
            )
        ]
        return sorted(merge_docked_passes(passes), key=lambda visible_pass: visible_pass.starts_at)
