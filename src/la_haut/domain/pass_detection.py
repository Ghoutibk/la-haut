from collections.abc import Sequence
from itertools import groupby

from la_haut.domain.sky_sample import SkySample
from la_haut.domain.visibility import NakedEyeVisibility
from la_haut.domain.visible_pass import VisiblePass


def detect_visible_passes(
    satellite_name: str,
    samples: Sequence[SkySample],
    visibility: NakedEyeVisibility,
) -> list[VisiblePass]:
    """Découpe une trace chronologique en passages visibles consécutifs."""
    passes = []
    for is_visible, run in groupby(samples, key=visibility.allows):
        if is_visible:
            passes.append(_pass_from(satellite_name, list(run)))
    return passes


def _pass_from(satellite_name: str, run: list[SkySample]) -> VisiblePass:
    first, last = run[0], run[-1]
    return VisiblePass(
        satellite_name=satellite_name,
        starts_at=first.at,
        ends_at=last.at,
        appears_in=first.direction,
        vanishes_in=last.direction,
        max_elevation_deg=max(sample.elevation_deg for sample in run),
        path=tuple(run),
    )
