from dataclasses import dataclass

MAX_ABS_LATITUDE_DEG = 90.0
MAX_ABS_LONGITUDE_DEG = 180.0


class InvalidObserverError(ValueError):
    """Un observateur doit se tenir quelque part sur Terre."""


@dataclass(frozen=True, slots=True)
class Observer:
    """La personne qui regarde le ciel, à un point précis du globe."""

    latitude_deg: float
    longitude_deg: float
    altitude_m: float = 0.0

    def __post_init__(self) -> None:
        if abs(self.latitude_deg) > MAX_ABS_LATITUDE_DEG:
            raise InvalidObserverError(f"Latitude hors de [-90, 90] : {self.latitude_deg}")
        if abs(self.longitude_deg) > MAX_ABS_LONGITUDE_DEG:
            raise InvalidObserverError(f"Longitude hors de [-180, 180] : {self.longitude_deg}")
