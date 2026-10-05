"""Racine de composition : seul endroit qui connaît cas d'usage et adaptateurs à la fois."""

from pathlib import Path

from la_haut.application.famous_satellite_catalog import FamousSatelliteCatalog
from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.application.ports import SatelliteCatalog
from la_haut.infrastructure.celestrak_satellite_catalog import (
    CELESTRAK_GP_URL,
    CelestrakSatelliteCatalog,
)
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog


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
