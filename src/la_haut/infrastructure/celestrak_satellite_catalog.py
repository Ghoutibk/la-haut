import ssl
import urllib.parse
import urllib.request
from pathlib import Path

import certifi

from la_haut.domain.satellite import Satellite
from la_haut.infrastructure.tle_file_satellite_catalog import parse_three_line_catalog

CELESTRAK_GP_URL = "https://celestrak.org/NORAD/elements/gp.php"
BRIGHTEST_SATELLITES_GROUP = "visual"
DOWNLOAD_TIMEOUT_S = 30


class CelestrakSatelliteCatalog:
    """Adaptateur SatelliteCatalog : un groupe CelesTrak téléchargé et gardé en cache sur disque.

    Par défaut, le groupe « visual » : la centaine de satellites les plus brillants.
    """

    def __init__(
        self,
        cache_path: Path,
        group: str = BRIGHTEST_SATELLITES_GROUP,
        base_url: str = CELESTRAK_GP_URL,
    ) -> None:
        self._cache_path = cache_path
        self._group = group
        self._base_url = base_url

    def tracked_satellites(self) -> list[Satellite]:
        text = self._download()
        self._cache_path.write_text(text, encoding="utf-8")
        return parse_three_line_catalog(text)

    def _download(self) -> str:
        query = urllib.parse.urlencode({"GROUP": self._group, "FORMAT": "tle"})
        context = ssl.create_default_context(cafile=certifi.where())
        url = f"{self._base_url}?{query}"
        with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT_S, context=context) as response:
            return response.read().decode("utf-8")
