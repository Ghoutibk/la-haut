"""L'API HTTP de Là-haut. Elle ne connaît que les cas d'usage, jamais les adaptateurs."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse

from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.ports import CatalogUnavailableError
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.observer import Observer
from la_haut.domain.sighting import InvalidSightingError, Sighting
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

    @app.exception_handler(InvalidSightingError)
    def reject_invalid_sighting(_: Request, error: InvalidSightingError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(error)})

    @app.exception_handler(CatalogUnavailableError)
    def report_unavailable_catalog(_: Request, __: CatalogUnavailableError) -> JSONResponse:
        detail = "Le catalogue des satellites est indisponible pour le moment, réessaie plus tard."
        return JSONResponse(status_code=503, content={"detail": detail})

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

    @app.get("/api/identification")
    def what_was_that(
        latitude: Latitude,
        longitude: Longitude,
        at: datetime,
        direction: CompassPoint,
    ) -> dict:
        observer = Observer(latitude_deg=latitude, longitude_deg=longitude)
        sighting = Sighting(at=at, direction=direction)
        return {
            "candidates": [present_pass(p) for p in identify_sighting.execute(observer, sighting)]
        }

    return app
