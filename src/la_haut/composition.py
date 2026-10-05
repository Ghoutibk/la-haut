"""Racine de composition : seul endroit qui connaît cas d'usage et adaptateurs à la fois."""

import os
from pathlib import Path

from fastapi import FastAPI

from la_haut.application.famous_satellite_catalog import FamousSatelliteCatalog
from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.ports import SatelliteCatalog
from la_haut.infrastructure.celestrak_satellite_catalog import (
    CELESTRAK_GP_URL,
    CelestrakSatelliteCatalog,
)
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog
from la_haut.interface.http.app import create_app

DEFAULT_CACHE_PATH = Path.home() / ".cache" / "la-haut" / "visual.tle"


def _list_visible_passes(catalog: SatelliteCatalog) -> ListVisiblePasses:
    return ListVisiblePasses(catalog=catalog, tracker=SkyfieldSkyTracker())


def build_list_visible_passes(catalog_path: Path) -> ListVisiblePasses:
    """Les satellites d'un fichier TLE local."""
    return _list_visible_passes(TleFileSatelliteCatalog(catalog_path))


def build_list_visible_passes_from_celestrak(
    cache_path: Path, base_url: str = CELESTRAK_GP_URL
) -> ListVisiblePasses:
    """Les satellites célèbres, avec leurs éléments tenus à jour depuis CelesTrak."""
    brightest = CelestrakSatelliteCatalog(cache_path, base_url=base_url)
    return _list_visible_passes(FamousSatelliteCatalog(brightest))


def build_identify_sighting(catalog_path: Path) -> IdentifySighting:
    """« C'était quoi, ça ? » parmi les satellites d'un fichier TLE local."""
    return IdentifySighting(build_list_visible_passes(catalog_path))


def build_identify_sighting_from_celestrak(
    cache_path: Path, base_url: str = CELESTRAK_GP_URL
) -> IdentifySighting:
    """« C'était quoi, ça ? » parmi les satellites célèbres tenus à jour depuis CelesTrak."""
    return IdentifySighting(build_list_visible_passes_from_celestrak(cache_path, base_url))


def build_web_app(cache_path: Path | None = None, base_url: str = CELESTRAK_GP_URL) -> FastAPI:
    """Le site Là-haut : uvicorn --factory la_haut.composition:build_web_app

    Le cache CelesTrak se règle avec la variable d'environnement LA_HAUT_CACHE.
    """
    cache_path = cache_path or Path(os.environ.get("LA_HAUT_CACHE", DEFAULT_CACHE_PATH))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    list_visible_passes = build_list_visible_passes_from_celestrak(cache_path, base_url)
    return create_app(list_visible_passes, IdentifySighting(list_visible_passes))
