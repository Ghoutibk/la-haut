import threading
from collections import OrderedDict
from datetime import UTC, datetime, timedelta

from la_haut.application.ports import VisiblePassesListing
from la_haut.domain.observer import Observer
from la_haut.domain.time_window import TimeWindow
from la_haut.domain.visible_pass import VisiblePass

SLOT = timedelta(minutes=15)
DEFAULT_CAPACITY = 256
_SLOTS_ORIGIN = datetime(2000, 1, 1, tzinfo=UTC)


def _slot_start(instant: datetime, slot: timedelta) -> datetime:
    return instant - (instant - _SLOTS_ORIGIN) % slot


def _slot_end(instant: datetime, slot: timedelta) -> datetime:
    start = _slot_start(instant, slot)
    return start if start == instant else start + slot


class ListVisiblePassesBySlot:
    """Cas d'usage décoré : « Ce soir » se calcule par créneaux d'un quart d'heure.

    Les passages sont calculés une fois pour les quarts d'heure qui couvrent la fenêtre, puis
    resservis à chaque visite du même observateur dans le même créneau, limités à sa fenêtre.
    Les créneaux les plus anciens sont oubliés au-delà de la capacité.
    """

    def __init__(
        self,
        list_visible_passes: VisiblePassesListing,
        slot: timedelta = SLOT,
        capacity: int = DEFAULT_CAPACITY,
    ) -> None:
        self._list_visible_passes = list_visible_passes
        self._slot = slot
        self._capacity = capacity
        self._passes_by_slot: OrderedDict[tuple[Observer, TimeWindow], list[VisiblePass]] = (
            OrderedDict()
        )
        # Les requêtes arrivent en parallèle : un même créneau ne se calcule qu'une fois.
        self._lock = threading.Lock()

    def execute(self, observer: Observer, window: TimeWindow) -> list[VisiblePass]:
        slots = TimeWindow(
            starts_at=_slot_start(window.starts_at, self._slot),
            ends_at=_slot_end(window.ends_at, self._slot),
        )
        with self._lock:
            passes = self._passes_of(observer, slots)
        return [
            visible_pass
            for visible_pass in passes
            if visible_pass.ends_at >= window.starts_at and visible_pass.starts_at <= window.ends_at
        ]

    def _passes_of(self, observer: Observer, slots: TimeWindow) -> list[VisiblePass]:
        key = (observer, slots)
        if key in self._passes_by_slot:
            self._passes_by_slot.move_to_end(key)
        else:
            self._passes_by_slot[key] = self._list_visible_passes.execute(observer, slots)
            if len(self._passes_by_slot) > self._capacity:
                self._passes_by_slot.popitem(last=False)
        return self._passes_by_slot[key]
