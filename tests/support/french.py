"""Lecture des dates, heures et directions écrites en français dans les scénarios."""

import re
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.planet import Planet

PARIS_TIME = ZoneInfo("Europe/Paris")
MONTHS = {
    name: number
    for number, name in enumerate(
        [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ],
        start=1,
    )
}
DIRECTIONS = {
    "nord": CompassPoint.NORTH,
    "nord-est": CompassPoint.NORTH_EAST,
    "est": CompassPoint.EAST,
    "sud-est": CompassPoint.SOUTH_EAST,
    "sud": CompassPoint.SOUTH,
    "sud-ouest": CompassPoint.SOUTH_WEST,
    "ouest": CompassPoint.WEST,
    "nord-ouest": CompassPoint.NORTH_WEST,
}


def french_date(text: str) -> date:
    """« 4 juillet 2018 » → date."""
    day, month, year = text.split()
    return date(int(year), MONTHS[month], int(day))


def paris_instant(day: date, clock: time) -> datetime:
    return datetime.combine(day, clock, tzinfo=PARIS_TIME)


def paris_instant_from_hour_text(text: str) -> datetime:
    """« 4 juillet 2018 à 3 h » → instant à Paris."""
    match = re.fullmatch(r"(?P<day>.+) à (?P<hour>\d{1,2}) h", text)
    return paris_instant(french_date(match["day"]), time(int(match["hour"])))


PLANETS = {
    "Vénus": Planet.VENUS,
    "Mars": Planet.MARS,
    "Jupiter": Planet.JUPITER,
    "Saturne": Planet.SATURN,
}
