from collections.abc import Sequence
from dataclasses import replace
from datetime import timedelta

from la_haut.domain.visible_pass import VisiblePass

SAME_PATH_TIME_TOLERANCE = timedelta(seconds=30)
SAME_PATH_ELEVATION_TOLERANCE_DEG = 1.0


def _on_the_same_path(first: VisiblePass, second: VisiblePass) -> bool:
    return (
        abs(first.starts_at - second.starts_at) <= SAME_PATH_TIME_TOLERANCE
        and abs(first.ends_at - second.ends_at) <= SAME_PATH_TIME_TOLERANCE
        and abs(first.max_elevation_deg - second.max_elevation_deg)
        <= SAME_PATH_ELEVATION_TOLERANCE_DEG
    )


def merge_docked_passes(passes: Sequence[VisiblePass]) -> list[VisiblePass]:
    """Des objets amarrés forment un seul point lumineux : un seul passage, au nom du premier."""
    merged: list[VisiblePass] = []
    for visible_pass in passes:
        for index, kept in enumerate(merged):
            if _on_the_same_path(kept, visible_pass):
                docked_with = (*kept.docked_with, visible_pass.satellite_name)
                merged[index] = replace(kept, docked_with=docked_with)
                break
        else:
            merged.append(visible_pass)
    return merged
