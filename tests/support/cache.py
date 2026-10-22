"""Un catalogue gardé sur le disque : son âge est la date de modification de son fichier."""

import os
import time
from pathlib import Path

THREE_HOURS_S = 3 * 3600


def a_cache_written(path: Path, catalog: str, seconds_ago: float = 0) -> None:
    """Écrit le catalogue comme s'il avait été téléchargé il y a `seconds_ago` secondes."""
    path.write_text(catalog, "utf-8")
    written_at = time.time() - seconds_ago
    os.utime(path, (written_at, written_at))
