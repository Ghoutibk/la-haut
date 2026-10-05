"""Configuration commune des tests : affiche la pyramide de tests en fin de session."""

from collections import Counter

PYRAMID_TARGETS = {"unit": 80, "integration": 13, "functional": 7}


def _test_family(node_id: str) -> str | None:
    parts = node_id.split("/")
    if len(parts) < 2 or parts[0] != "tests":
        return None
    family = parts[1]
    return family if family in PYRAMID_TARGETS else None


def pytest_terminal_summary(terminalreporter):
    counts = Counter()
    for outcome in ("passed", "failed"):
        for report in terminalreporter.stats.get(outcome, []):
            if getattr(report, "when", "call") != "call":
                continue
            family = _test_family(report.nodeid)
            if family:
                counts[family] += 1

    total = sum(counts.values())
    if total == 0:
        return

    terminalreporter.write_sep("-", "Pyramide de tests (cible 80 / 13 / 7)")
    for family, target in PYRAMID_TARGETS.items():
        share = 100 * counts[family] / total
        terminalreporter.write_line(
            f"{family:<12} {counts[family]:>4} tests  {share:5.1f} %  (cible {target} %)"
        )
