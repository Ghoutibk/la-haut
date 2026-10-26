"""Une page factice, rangée comme Vite range la vraie : la page, et ses scripts sous assets/."""

from pathlib import Path

A_SCRIPT = "assets/page.js"


def a_static_dir(root: Path) -> Path:
    (root / "assets").mkdir(parents=True)
    (root / "index.html").write_text("<!doctype html><title>Là-haut</title>", encoding="utf-8")
    (root / A_SCRIPT).write_text("export {};\n", encoding="utf-8")
    return root
