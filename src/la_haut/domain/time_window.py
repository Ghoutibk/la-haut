from dataclasses import dataclass
from datetime import datetime, timedelta


class InvalidTimeWindowError(ValueError):
    """Une fenêtre d'observation doit avoir un début et une fin cohérents."""


@dataclass(frozen=True, slots=True)
class TimeWindow:
    """La période pendant laquelle on cherche des passages, par exemple « ce soir »."""

    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        if self.starts_at.tzinfo is None or self.ends_at.tzinfo is None:
            raise InvalidTimeWindowError("Les instants doivent porter un fuseau horaire")
        if self.ends_at <= self.starts_at:
            raise InvalidTimeWindowError("La fenêtre doit finir après avoir commencé")

    @property
    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at
