import re
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from pytest_bdd import given, parsers, scenarios, then, when

from la_haut.composition import build_list_visible_passes
from la_haut.domain.compass_point import CompassPoint
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import an_observer_in_paris
from tests.support.fixtures import ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2

scenarios("passages_visibles.feature")

PARIS_TIME = ZoneInfo("Europe/Paris")
TOLERANCE = timedelta(minutes=1)
MONTHS = {
    name: number
    for number, name in enumerate(
        [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ],
        start=1,
    )
}
DIRECTIONS = {
    "nord": CompassPoint.NORTH,
    "nord-est": CompassPoint.NORTH_EAST,
    "est": CompassPoint.EAST,
    "sud-est": CompassPoint.SOUTH_EAST,
    "sud": CompassPoint.SOUTH,
    "sud-ouest": CompassPoint.SOUTH_WEST,
    "ouest": CompassPoint.WEST,
    "nord-ouest": CompassPoint.NORTH_WEST,
}


def french_date(text: str) -> date:
    day, month, year = text.split()
    return date(int(year), MONTHS[month], int(day))


def paris_instant(day: date, clock: time) -> datetime:
    return datetime.combine(day, clock, tzinfo=PARIS_TIME)


def paris_instant_from_hour_text(text: str) -> datetime:
    """« 4 juillet 2018 à 3 h » → instant à Paris."""
    match = re.fullmatch(r"(?P<day>.+) à (?P<hour>\d{1,2}) h", text)
    return paris_instant(french_date(match["day"]), time(int(match["hour"])))


@given("un observateur à Paris", target_fixture="observer")
def observer():
    return an_observer_in_paris()


@given(
    "un catalogue qui suit l'ISS avec ses éléments orbitaux du 3 juillet 2018",
    target_fixture="catalog_path",
)
def catalog_path(tmp_path):
    path = tmp_path / "stations.tle"
    path.write_text("\n".join([ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2]) + "\n", "utf-8")
    return path


@when(
    parsers.parse("je cherche les passages visibles du {start} au {end}"),
    target_fixture="passes",
)
def search_visible_passes(observer, catalog_path, start, end):
    window = TimeWindow(
        starts_at=paris_instant_from_hour_text(start),
        ends_at=paris_instant_from_hour_text(end),
    )
    return build_list_visible_passes(catalog_path).execute(observer, window)


@then("je ne vois aucun passage")
def no_pass_is_announced(passes):
    assert passes == []


@then("je vois ces passages :")
def these_passes_are_announced(passes, datatable):
    header, *rows = datatable
    expected_passes = [dict(zip(header, row, strict=True)) for row in rows]

    assert len(passes) == len(expected_passes)
    for visible_pass, expected in zip(passes, expected_passes, strict=True):
        day = french_date(expected["jour"])
        assert visible_pass.satellite_name == expected["satellite"]
        expected_start = paris_instant(day, time.fromisoformat(expected["début"]))
        expected_end = paris_instant(day, time.fromisoformat(expected["fin"]))
        assert abs(visible_pass.starts_at - expected_start) <= TOLERANCE
        assert abs(visible_pass.ends_at - expected_end) <= TOLERANCE
        assert visible_pass.appears_in == DIRECTIONS[expected["depuis"]]
        assert visible_pass.vanishes_in == DIRECTIONS[expected["vers"]]
