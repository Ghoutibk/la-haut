"""L'API HTTP de Là-haut. Elle ne connaît que les cas d'usage, jamais les adaptateurs."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from la_haut.application.ports import (
    CatalogUnavailableError,
    FeedbackNotConfiguredError,
    FeedbackUnavailableError,
    SightingIdentification,
    VisiblePassesListing,
)
from la_haut.application.send_feedback import FeedbackLimitReachedError, SendFeedback
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.feedback import Feedback, FeedbackKind, InvalidFeedbackError
from la_haut.domain.observer import Observer
from la_haut.domain.sighting import InvalidSightingError, Sighting
from la_haut.domain.time_window import TimeWindow
from la_haut.interface.http.presenters import present_identification, present_pass

Latitude = Annotated[float, Query(ge=-90, le=90)]
Longitude = Annotated[float, Query(ge=-180, le=180)]
DEFAULT_HOURS_AHEAD = 12
MAX_HOURS_AHEAD = 48
STATIC_DIR = Path(__file__).parent / "static"


# Garde-fou de transport : le domaine fixe les vraies limites, avec un message lisible.
MAX_FEEDBACK_FIELD_LENGTH = 10_000


class FeedbackForm(BaseModel):
    """Le formulaire « Ton avis » de la page."""

    kind: FeedbackKind
    message: str = Field(max_length=MAX_FEEDBACK_FIELD_LENGTH)
    contact: str | None = Field(default=None, max_length=MAX_FEEDBACK_FIELD_LENGTH)
    # Piège à robots : un champ caché aux humains, que seuls les robots remplissent.
    website: str = ""


def _utc_now() -> datetime:
    return datetime.now(UTC)


def create_app(
    list_visible_passes: VisiblePassesListing,
    identify_sighting: SightingIdentification,
    clock: Callable[[], datetime] = _utc_now,
    send_feedback: SendFeedback | None = None,
) -> FastAPI:
    app = FastAPI(title="Là-haut")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def web_page() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health", include_in_schema=False)
    def health() -> dict:
        """Pour l'hébergeur : le service répond, sans rien calculer ni télécharger."""
        return {"status": "ok"}

    @app.exception_handler(InvalidSightingError)
    def reject_invalid_sighting(_: Request, error: InvalidSightingError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(error)})

    @app.exception_handler(CatalogUnavailableError)
    def report_unavailable_catalog(_: Request, __: CatalogUnavailableError) -> JSONResponse:
        detail = "Le catalogue des satellites est indisponible pour le moment, réessaie plus tard."
        return JSONResponse(status_code=503, content={"detail": detail})

    @app.exception_handler(InvalidFeedbackError)
    def reject_invalid_feedback(_: Request, error: InvalidFeedbackError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(error)})

    @app.exception_handler(FeedbackUnavailableError)
    def report_unavailable_feedback(_: Request, __: FeedbackUnavailableError) -> JSONResponse:
        detail = "L'envoi des avis est indisponible pour le moment, réessaie plus tard."
        return JSONResponse(status_code=503, content={"detail": detail})

    @app.exception_handler(FeedbackNotConfiguredError)
    def report_unconfigured_feedback(_: Request, __: FeedbackNotConfiguredError) -> JSONResponse:
        detail = "L'envoi des avis n'est pas encore configuré sur ce site."
        return JSONResponse(status_code=503, content={"detail": detail})

    @app.exception_handler(FeedbackLimitReachedError)
    def ask_to_wait(_: Request, __: FeedbackLimitReachedError) -> JSONResponse:
        detail = "Beaucoup de messages viennent d'arriver : réessaie dans un moment."
        return JSONResponse(status_code=429, content={"detail": detail})

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
        return present_identification(identify_sighting.execute(observer, sighting))

    @app.post("/api/feedback", status_code=201)
    def send_a_feedback(form: FeedbackForm) -> dict:
        if form.website:
            return {"status": "sent"}  # un robot : on fait comme si, et rien ne part
        if send_feedback is None:
            raise FeedbackUnavailableError("Aucune boîte à avis")
        send_feedback.execute(Feedback(form.kind, form.message, form.contact))
        return {"status": "sent"}

    return app
