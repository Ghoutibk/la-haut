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


def _public_name(visible_pass: VisiblePass) -> str:
    if visible_pass.is_starlink_train:
        return f"Train Starlink ({visible_pass.train_size} satellites)"
    return PUBLIC_NAMES.get(visible_pass.satellite_name, visible_pass.satellite_name)


def present_pass(visible_pass: VisiblePass) -> dict:
    return {
        "kind": "train" if visible_pass.is_starlink_train else "satellite",
        "name": _public_name(visible_pass),
        "satellite": visible_pass.satellite_name,
        "docked_with": list(visible_pass.docked_with),
        "starts_at": visible_pass.starts_at.isoformat(),
        "ends_at": visible_pass.ends_at.isoformat(),
        "duration_s": round(visible_pass.duration.total_seconds()),
        "appears_in": _present_direction(visible_pass.appears_in),
        "vanishes_in": _present_direction(visible_pass.vanishes_in),
        "max_elevation_deg": round(visible_pass.max_elevation_deg),
    }
