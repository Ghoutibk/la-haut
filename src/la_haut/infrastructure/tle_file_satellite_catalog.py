from pathlib import Path

from la_haut.domain.satellite import Satellite, TwoLineElements

LINES_PER_ENTRY = 3


class TleFileSatelliteCatalog:
    """Adaptateur SatelliteCatalog : un fichier TLE à trois lignes, au format CelesTrak."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def tracked_satellites(self) -> list[Satellite]:
        text = self._path.read_text(encoding="utf-8")
        lines = [line.rstrip() for line in text.splitlines() if line.strip()]
        entries = [
            lines[start : start + LINES_PER_ENTRY]
            for start in range(0, len(lines), LINES_PER_ENTRY)
        ]
        return [
            Satellite(name=name.strip(), elements=TwoLineElements(line_1, line_2))
            for name, line_1, line_2 in entries
        ]
