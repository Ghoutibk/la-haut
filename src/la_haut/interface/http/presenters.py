"""Traduction des objets du domaine en JSON pour la page web."""

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.visible_pass import VisiblePass

FRENCH_COMPASS_NAMES = {
    CompassPoint.NORTH: "nord",
    CompassPoint.NORTH_EAST: "nord-est",
    CompassPoint.EAST: "est",
    CompassPoint.SOUTH_EAST: "sud-est",
    CompassPoint.SOUTH: "sud",
    CompassPoint.SOUTH_WEST: "sud-ouest",
    CompassPoint.WEST: "ouest",
    CompassPoint.NORTH_WEST: "nord-ouest",
}

PUBLIC_NAMES = {
    "ISS (ZARYA)": "Station spatiale internationale",
    "CSS (TIANHE)": "Station spatiale chinoise Tiangong",
    "HST": "Télescope spatial Hubble",
}


def _present_direction(point: CompassPoint) -> dict[str, str]:
    return {"code": point.value, "label": FRENCH_COMPASS_NAMES[point]}


def present_pass(visible_pass: VisiblePass) -> dict:
    return {
        "name": PUBLIC_NAMES.get(visible_pass.satellite_name, visible_pass.satellite_name),
        "satellite": visible_pass.satellite_name,
        "docked_with": list(visible_pass.docked_with),
        "starts_at": visible_pass.starts_at.isoformat(),
        "ends_at": visible_pass.ends_at.isoformat(),
        "duration_s": round(visible_pass.duration.total_seconds()),
        "appears_in": _present_direction(visible_pass.appears_in),
        "vanishes_in": _present_direction(visible_pass.vanishes_in),
        "max_elevation_deg": round(visible_pass.max_elevation_deg),
    }
