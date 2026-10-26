"""La page de Là-haut, construite par Vite depuis frontend/ dans le dossier que le site sert."""

import subprocess
from pathlib import Path

from la_haut.composition import STATIC_DIR

FRONTEND = Path(__file__).parents[2] / "frontend"


def _sources() -> list[Path]:
    return [
        path
        for path in FRONTEND.rglob("*")
        if path.is_file() and "node_modules" not in path.relative_to(FRONTEND).parts
    ]


def is_stale() -> bool:
    """Vrai si la page n'est pas construite, ou l'est d'après des sources plus anciennes."""
    page = STATIC_DIR / "index.html"
    if not page.exists():
        return True
    built_at = page.stat().st_mtime
    return any(source.stat().st_mtime > built_at for source in _sources())


def build() -> None:
    subprocess.run(["npm", "--prefix", str(FRONTEND), "run", "build"], check=True)
