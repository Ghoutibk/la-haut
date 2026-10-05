from enum import StrEnum

DEGREES_PER_POINT = 45.0
FULL_TURN_DEG = 360.0


class InvalidAzimuthError(ValueError):
    """Un azimut doit être compris dans [0, 360[ degrés."""


class CompassPoint(StrEnum):
    """Un des huit points de la rose des vents, dans le sens horaire depuis le nord."""

    NORTH = "N"
    NORTH_EAST = "NE"
    EAST = "E"
    SOUTH_EAST = "SE"
    SOUTH = "S"
    SOUTH_WEST = "SW"
    WEST = "W"
    NORTH_WEST = "NW"

    @classmethod
    def from_azimuth(cls, azimuth_deg: float) -> "CompassPoint":
        if not 0 <= azimuth_deg < FULL_TURN_DEG:
            raise InvalidAzimuthError(f"Azimut hors de [0, 360[ : {azimuth_deg}")
        points = list(cls)
        index = int((azimuth_deg + DEGREES_PER_POINT / 2) // DEGREES_PER_POINT) % len(points)
        return points[index]
