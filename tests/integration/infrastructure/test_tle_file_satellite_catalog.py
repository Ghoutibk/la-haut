import pytest

from la_haut.domain.satellite import InvalidTwoLineElementsError
from la_haut.infrastructure.tle_file_satellite_catalog import TleFileSatelliteCatalog
from tests.support.fixtures import ISS_TLE_LINE_1, ISS_TLE_LINE_2

# Second satellite réel, tel que publié par CelesTrak (nom complété par des espaces).
FLOCK_NAME_LINE = "FLOCK 2E-1              "
FLOCK_TLE_LINE_1 = "1 41483U 98067JD  18135.38689952  .00096183  14684-4  28212-3 0  9990"
FLOCK_TLE_LINE_2 = "2 41483  51.6270 103.3896 0004826  61.7810 298.3684 15.92672255114129"


def a_catalog_file(tmp_path, *lines, newline="\n"):
    path = tmp_path / "stations.tle"
    path.write_bytes((newline.join(lines) + newline).encode("utf-8"))
    return path


def test_every_satellite_of_a_celestrak_three_line_file_is_tracked(tmp_path):
    path = a_catalog_file(
        tmp_path,
        "ISS (ZARYA)             ",
        ISS_TLE_LINE_1,
        ISS_TLE_LINE_2,
        FLOCK_NAME_LINE,
        FLOCK_TLE_LINE_1,
        FLOCK_TLE_LINE_2,
    )

    satellites = TleFileSatelliteCatalog(path).tracked_satellites()

    assert [(satellite.name, satellite.norad_id) for satellite in satellites] == [
        ("ISS (ZARYA)", 25544),
        ("FLOCK 2E-1", 41483),
    ]


def test_windows_line_endings_and_blank_lines_are_tolerated(tmp_path):
    path = a_catalog_file(
        tmp_path, "", "ISS (ZARYA)", ISS_TLE_LINE_1, ISS_TLE_LINE_2, "", newline="\r\n"
    )

    [iss] = TleFileSatelliteCatalog(path).tracked_satellites()

    assert iss.norad_id == 25544


def test_a_corrupted_entry_is_refused_rather_than_tracked_wrongly(tmp_path):
    corrupted_line_1 = ISS_TLE_LINE_1[:-1] + "0"
    path = a_catalog_file(tmp_path, "ISS (ZARYA)", corrupted_line_1, ISS_TLE_LINE_2)

    with pytest.raises(InvalidTwoLineElementsError):
        TleFileSatelliteCatalog(path).tracked_satellites()
