from datetime import time, timedelta

from pytest_bdd import given, parsers, scenarios, then

from tests.support.fixtures import STARLINK_TRAIN
from tests.support.french import french_date, paris_instant

scenarios("trains_starlink.feature")

TOLERANCE = timedelta(minutes=1)


@given(
    "un catalogue qui suit trois Starlink d'un même lancement, à quinze secondes l'un de l'autre",
    target_fixture="catalog_path",
)
def a_starlink_train_catalog(tmp_path):
    path = tmp_path / "starlink.tle"
    path.write_text("\n".join(line for entry in STARLINK_TRAIN for line in entry) + "\n", "utf-8")
    return path


@then(
    parsers.parse(
        "je vois un seul passage, un train Starlink de {size:d} satellites, "
        "le {day} de {start} à {end}"
    )
)
def one_train_pass(passes, size, day, start, end):
    [train] = passes
    assert (train.is_starlink_train, train.train_size) == (True, size)
    expected_start = paris_instant(french_date(day), time.fromisoformat(start))
    expected_end = paris_instant(french_date(day), time.fromisoformat(end))
    assert abs(train.starts_at - expected_start) <= TOLERANCE
    assert abs(train.ends_at - expected_end) <= TOLERANCE


@then(parsers.parse("la lumière était un train Starlink de {size:d} satellites"))
def it_was_a_train(identification, size):
    best = identification.candidates[0]
    assert (best.is_starlink_train, best.train_size) == (True, size)
