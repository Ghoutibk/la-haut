"""Racine de composition : seul endroit qui connaît cas d'usage et adaptateurs à la fois."""

from pathlib import Path

from la_haut.application.list_visible_passes import ListVisiblePasses
from la_haut.infrastructure.skyfield_sky_tracker import SkyfieldSkyTracker
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog


def build_list_visible_passes(catalog_path: Path) -> ListVisiblePasses:
    return ListVisiblePasses(
        catalog=TleFileSatelliteCatalog(catalog_path),
        tracker=SkyfieldSkyTracker(),
    )
