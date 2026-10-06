from collections.abc import Sequence
from dataclasses import replace
from datetime import timedelta

from la_haut.domain.starlink import is_starlink
from la_haut.domain.visible_pass import VisiblePass

# Les satellites d'un train défilent l'un derrière l'autre : leurs passages se chevauchent.
TRAIN_MAX_GAP = timedelta(minutes=1)
# Un peu plus large que pour des objets amarrés : la Terre tourne entre deux satellites de la file.
TRAIN_ELEVATION_TOLERANCE_DEG = 5.0


def _follows(train: VisiblePass, candidate: VisiblePass) -> bool:
    return (
        is_starlink(train.satellite_name)
        and is_starlink(candidate.satellite_name)
        and train.launch != ""
        and candidate.launch == train.launch
        and candidate.starts_at <= train.ends_at + TRAIN_MAX_GAP
        and candidate.ends_at >= train.starts_at - TRAIN_MAX_GAP
        and abs(candidate.max_elevation_deg - train.max_elevation_deg)
        <= TRAIN_ELEVATION_TOLERANCE_DEG
        and candidate.appears_in.is_close_to(train.appears_in)
        and candidate.vanishes_in.is_close_to(train.vanishes_in)
    )


def _join(train: VisiblePass, follower: VisiblePass) -> VisiblePass:
    first = min(train, follower, key=lambda visible_pass: visible_pass.starts_at)
    last = max(train, follower, key=lambda visible_pass: visible_pass.ends_at)
    return replace(
        train,
        starts_at=first.starts_at,
        appears_in=first.appears_in,
        ends_at=last.ends_at,
        vanishes_in=last.vanishes_in,
        max_elevation_deg=max(train.max_elevation_deg, follower.max_elevation_deg),
        path=tuple(sorted((*train.path, *follower.path), key=lambda sample: sample.at)),
        train_followers=(*train.train_followers, follower.satellite_name),
    )


def gather_starlink_trains(passes: Sequence[VisiblePass]) -> list[VisiblePass]:
    """Les Starlink d'un même lancement qui défilent en file : un seul passage de train.

    La file se lit dans l'ordre où les satellites passent, quel que soit l'ordre du catalogue.
    """
    gathered: list[VisiblePass] = []
    for visible_pass in sorted(passes, key=lambda visible_pass: visible_pass.starts_at):
        for index, train in enumerate(gathered):
            if _follows(train, visible_pass):
                gathered[index] = _join(train, visible_pass)
                break
        else:
            gathered.append(visible_pass)
    return gathered
