from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.observer import Observer
from la_haut.domain.sighting import SIGHTING_TIME_TOLERANCE, Sighting
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visible_pass import VisiblePass


class IdentifySighting:
    """Cas d'usage : « c'était quoi, ça ? » — les satellites qui collent au signalement."""

    def __init__(self, list_visible_passes: ListVisiblePasses) -> None:
        self._list_visible_passes = list_visible_passes

    def execute(self, observer: Observer, sighting: Sighting) -> list[VisiblePass]:
        around_the_sighting = TimeWindow(
            starts_at=sighting.at - SIGHTING_TIME_TOLERANCE,
            ends_at=sighting.at + SIGHTING_TIME_TOLERANCE,
        )
        gaps = {
            visible_pass: visible_pass.gap_to(sighting)
            for visible_pass in self._list_visible_passes.execute(observer, around_the_sighting)
        }
        return sorted(
            (visible_pass for visible_pass, gap in gaps.items() if gap is not None),
            key=lambda visible_pass: gaps[visible_pass],
        )
