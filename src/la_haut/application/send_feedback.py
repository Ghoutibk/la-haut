import threading
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from la_haut.application.ports import FeedbackInbox
from la_haut.domain.feedback import Feedback

ONE_HOUR = timedelta(hours=1)
# Bien plus que ce qu'envoient de vrais visiteurs : un plafond contre les envois en masse.
MAX_FEEDBACK_PER_HOUR = 20


class FeedbackLimitReachedError(RuntimeError):
    """Trop d'avis dans l'heure : la boîte à avis est protégée des envois en masse."""


def _utc_now() -> datetime:
    return datetime.now(UTC)


class SendFeedback:
    """Cas d'usage : remettre l'avis d'un visiteur à l'auteur du site, au plus tant par heure.

    Seuls les avis effectivement remis comptent dans la limite.
    """

    def __init__(
        self,
        inbox: FeedbackInbox,
        clock: Callable[[], datetime] = _utc_now,
        max_per_hour: int = MAX_FEEDBACK_PER_HOUR,
    ) -> None:
        self._inbox = inbox
        self._clock = clock
        self._max_per_hour = max_per_hour
        self._delivered_at: list[datetime] = []
        self._lock = threading.Lock()

    def execute(self, feedback: Feedback) -> None:
        with self._lock:
            now = self._clock()
            self._delivered_at = [at for at in self._delivered_at if now - at < ONE_HOUR]
            if len(self._delivered_at) >= self._max_per_hour:
                raise FeedbackLimitReachedError("Trop d'avis dans l'heure")
            self._inbox.deliver(feedback, now)
            self._delivered_at.append(now)
