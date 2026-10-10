from pytest_bdd import parsers, scenarios, then

from tests.support.french import is_about

scenarios("trains_starlink_reels.feature")


@then(
    parsers.parse("je vois un train Starlink de {size:d} satellites, le {day} de {start} à {end}")
)
def a_train_among_the_passes(passes, size, day, start, end):
    assert any(
        visible_pass.train_size == size
        and is_about(visible_pass.starts_at, day, start)
        and is_about(visible_pass.ends_at, day, end)
        for visible_pass in passes
    )
