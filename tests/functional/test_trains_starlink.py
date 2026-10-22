from pytest_bdd import given, parsers, scenarios, then

from tests.support.fixtures import STARLINK_TRAIN
from tests.support.french import is_about

scenarios("trains_starlink.feature")


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
    assert is_about(train.starts_at, day, start)
    assert is_about(train.ends_at, day, end)


@then(parsers.parse("la lumière était un train Starlink de {size:d} satellites"))
def it_was_a_train(identification, size):
    best = identification.candidates[0]
    assert (best.is_starlink_train, best.train_size) == (True, size)
