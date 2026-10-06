"""Racine de composition : seul endroit qui connaît cas d'usage et adaptateurs à la fois."""

import os
from pathlib import Path

from fastapi import FastAPI

from la_haut.application.combined_satellite_catalog import CombinedSatelliteCatalog
from la_haut.application.famous_satellite_catalog import FamousSatelliteCatalog
from la_haut.application.identify_sighting import IdentifySighting
from la_haut.application.identify_sighting_with_planets import IdentifySightingWithPlanets
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.ports import SatelliteCatalog
from la_haut.application.starlink_catalog import StarlinkCatalog
from la_haut.infrastructure.celestrak_satellite_catalog import (
    CELESTRAK_URL_TEMPLATE,
    CelestrakSatelliteCatalog,
)
from la_haut.infrastructure.skyfield_planet_locator import SkyfieldPlanetLocator
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog
from la_haut.interface.http.app import create_app

DEFAULT_CACHE_PATH = Path.home() / ".cache" / "la-haut" / "visual.tle"
# Les lancements des 30 derniers jours : les Starlink qui défilent encore en train.
RECENT_LAUNCHES_GROUP = "last-30-days"


def _list_visible_passes(catalog: SatelliteCatalog) -> ListVisiblePasses:
    return ListVisiblePasses(catalog=catalog, tracker=SkyfieldSkyTracker())


def build_list_visible_passes(catalog_path: Path) -> ListVisiblePasses:
    """Les satellites d'un fichier TLE local."""
    return _list_visible_passes(TleFileSatelliteCatalog(catalog_path))


def build_list_visible_passes_from_celestrak(
    cache_path: Path, url_template: str = CELESTRAK_URL_TEMPLATE
) -> ListVisiblePasses:
    """Les satellites célèbres et les Starlink récents, tenus à jour depuis CelesTrak.

    Chaque groupe a son propre cache, dans le dossier de `cache_path`.
    """
    brightest = CelestrakSatelliteCatalog(cache_path, url_template=url_template)
    recent_launches = CelestrakSatelliteCatalog(
        cache_path.with_name(f"{RECENT_LAUNCHES_GROUP}.tle"),
        group=RECENT_LAUNCHES_GROUP,
        url_template=url_template,
    )
    catalog = CombinedSatelliteCatalog(
        FamousSatelliteCatalog(brightest), StarlinkCatalog(recent_launches)
    )
    return _list_visible_passes(catalog)


def _identify_sighting(list_visible_passes: ListVisiblePasses) -> IdentifySightingWithPlanets:
    return IdentifySightingWithPlanets(
        IdentifySighting(list_visible_passes), SkyfieldPlanetLocator()
    )


def build_identify_sighting(catalog_path: Path) -> IdentifySightingWithPlanets:
    """« C'était quoi, ça ? » parmi les satellites d'un fichier TLE local et les planètes."""
    return _identify_sighting(build_list_visible_passes(catalog_path))


def build_identify_sighting_from_celestrak(
    cache_path: Path, url_template: str = CELESTRAK_URL_TEMPLATE
) -> IdentifySightingWithPlanets:
    """« C'était quoi, ça ? » parmi les satellites suivis depuis CelesTrak et les planètes."""
    return _identify_sighting(build_list_visible_passes_from_celestrak(cache_path, url_template))


def build_web_app(
    cache_path: Path | None = None, url_template: str = CELESTRAK_URL_TEMPLATE
) -> FastAPI:
    """Le site Là-haut : uvicorn --factory la_haut.composition:build_web_app

    Le cache CelesTrak se règle avec la variable d'environnement LA_HAUT_CACHE.
    """
    cache_path = cache_path or Path(os.environ.get("LA_HAUT_CACHE", DEFAULT_CACHE_PATH))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    list_visible_passes = build_list_visible_passes_from_celestrak(cache_path, url_template)
    return create_app(list_visible_passes, _identify_sighting(list_visible_passes))
