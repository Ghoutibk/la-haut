"""Règle de dépendance de la Clean Architecture : les dépendances pointent vers le domaine."""

import ast
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "la_haut"


def _imported_modules(layer: str) -> set[str]:
    modules = set()
    for path in (PACKAGE_ROOT / layer).rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def _imports_outside(layer: str, allowed_packages: tuple[str, ...]) -> list[str]:
    return sorted(
        module
        for module in _imported_modules(layer)
        if module.split(".")[0] not in sys.stdlib_module_names
        and not module.startswith(allowed_packages)
    )


def test_the_domain_depends_only_on_itself_and_the_standard_library():
    assert _imports_outside("domain", ("la_haut.domain",)) == []


def test_the_application_depends_only_on_the_domain_and_the_standard_library():
    assert _imports_outside("application", ("la_haut.domain", "la_haut.application")) == []


def test_the_interface_never_reaches_the_adapters_directly():
    forbidden = ("la_haut.infrastructure", "la_haut.composition")

    assert [
        module for module in _imported_modules("interface") if module.startswith(forbidden)
    ] == []
