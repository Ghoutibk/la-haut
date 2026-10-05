"""L'API HTTP de Là-haut. Elle ne connaît que les cas d'usage, jamais les adaptateurs."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Query

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.domain.observer import Observer
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.presenters import present_pass

Latitude = Annotated[float, Query(ge=-90, le=90)]
Longitude = Annotated[float, Query(ge=-180, le=180)]
DEFAULT_HOURS_AHEAD = 12
MAX_HOURS_AHEAD = 48


def _utc_now() -> datetime:
    return datetime.now(UTC)


def create_app(
    list_visible_passes: ListVisiblePasses,
    identify_sighting: IdentifySighting,
    clock: Callable[[], datetime] = _utc_now,
) -> FastAPI:
    app = FastAPI(title="Là-haut")

    @app.get("/api/passes")
    def tonight(
        latitude: Latitude,
        longitude: Longitude,
        hours: Annotated[int, Query(ge=1, le=MAX_HOURS_AHEAD)] = DEFAULT_HOURS_AHEAD,
    ) -> dict:
        now = clock()
        window = TimeWindow(starts_at=now, ends_at=now + timedelta(hours=hours))
        observer = Observer(latitude_deg=latitude, longitude_deg=longitude)
        return {"passes": [present_pass(p) for p in list_visible_passes.execute(observer, window)]}

    return app
