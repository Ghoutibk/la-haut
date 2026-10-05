import ssl
import time
import urllib.parse
import urllib.request
from datetime import timedelta
from pathlib import Path

import certifi

from la_haut.application.ports import CatalogUnavailableError
from la_haut.domain.satellite import Satellite
from la_haut.infrastructure.tle_file_satellite_catalog import parse_three_line_catalog

CELESTRAK_GP_URL = "https://celestrak.org/NORAD/elements/gp.php"
BRIGHTEST_SATELLITES_GROUP = "visual"
DOWNLOAD_TIMEOUT_S = 30
# CelesTrak publie toutes les deux heures et demande de ne pas recharger plus souvent.
CELESTRAK_UPDATE_INTERVAL = timedelta(hours=2)


class CelestrakSatelliteCatalog:
    """Adaptateur SatelliteCatalog : un groupe CelesTrak téléchargé et gardé en cache sur disque.

    Par défaut, le groupe « visual » : la centaine de satellites les plus brillants.
    """

    def __init__(
        self,
        cache_path: Path,
        group: str = BRIGHTEST_SATELLITES_GROUP,
        base_url: str = CELESTRAK_GP_URL,
        max_age: timedelta = CELESTRAK_UPDATE_INTERVAL,
    ) -> None:
        self._cache_path = cache_path
        self._group = group
        self._base_url = base_url
        self._max_age = max_age

    def tracked_satellites(self) -> list[Satellite]:
        if not self._cache_is_fresh():
            self._refresh_cache()
        return parse_three_line_catalog(self._cache_path.read_text(encoding="utf-8"))

    def _cache_is_fresh(self) -> bool:
        if not self._cache_path.exists():
            return False
        age_s = time.time() - self._cache_path.stat().st_mtime
        return age_s < self._max_age.total_seconds()

    def _refresh_cache(self) -> None:
        try:
            text = self._download()
            if not parse_three_line_catalog(text):
                raise ValueError("Catalogue vide")
        except (OSError, ValueError) as error:
            if self._cache_path.exists():
                return  # le dernier catalogue connu reste valable en attendant
            raise CatalogUnavailableError("CelesTrak injoignable et aucun cache") from error
        self._cache_path.write_text(text, encoding="utf-8")

    def _download(self) -> str:
        query = urllib.parse.urlencode({"GROUP": self._group, "FORMAT": "tle"})
        context = ssl.create_default_context(cafile=certifi.where())
        url = f"{self._base_url}?{query}"
        with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT_S, context=context) as response:
            return response.read().decode("utf-8")
