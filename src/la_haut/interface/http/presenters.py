"""Traduction des objets du domaine en JSON pour la page web."""

from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.identification import Identification
from la_haut.domain.planet import Planet, PlanetPosition
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

FRENCH_PLANET_NAMES = {
    Planet.VENUS: "Vénus",
    Planet.JUPITER: "Jupiter",
    Planet.MARS: "Mars",
    Planet.SATURN: "Saturne",
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


def present_planet(position: PlanetPosition) -> dict:
    return {
        "kind": "planet",
        "name": FRENCH_PLANET_NAMES[position.planet],
        "planet": position.planet.value,
        "direction": _present_direction(position.direction),
        "elevation_deg": round(position.elevation_deg),
    }


def present_candidate(candidate: VisiblePass | PlanetPosition) -> dict:
    """Un candidat de « C'était quoi, ça ? » : un satellite, un train Starlink ou une planète."""
    if isinstance(candidate, PlanetPosition):
        return present_planet(candidate)
    return present_pass(candidate)


def present_identification(identification: Identification) -> dict:
    """La réponse à « C'était quoi, ça ? », et si les satellites ont pu être vérifiés."""
    return {
        "candidates": [present_candidate(candidate) for candidate in identification.candidates],
        "satellites_checked": identification.satellites_checked,
    }
