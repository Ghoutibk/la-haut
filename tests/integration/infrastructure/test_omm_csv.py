import pytest

from la_haut.domain.orbit_mean_elements import InvalidOrbitMeanElementsError
from la_haut.domain.starlink import is_starlink
from la_haut.infrastructure.omm_csv import parse_omm_csv
from tests.support.fixtures import LAST_30_DAYS_CSV_2026, VISUAL_CSV_2026


def test_the_recent_launches_are_read_with_their_numbers_beyond_99999():
    satellites = parse_omm_csv(LAST_30_DAYS_CSV_2026)

    assert len(satellites) == 170
    assert sum(is_starlink(satellite.name) for satellite in satellites) == 80
    assert min(satellite.norad_id for satellite in satellites) == 100615


def test_each_satellite_keeps_its_name_and_its_elements():
    iss = next(s for s in parse_omm_csv(VISUAL_CSV_2026) if s.norad_id == 25544)

    assert iss.name == "ISS (ZARYA)"
    assert iss.elements.as_fields()["EPOCH"] == "2026-10-06T12:44:07.877472"


def test_an_answer_without_data_holds_no_satellite():
    assert parse_omm_csv("No GP data found") == []


def test_a_row_missing_an_element_is_rejected():
    header, iss_row = VISUAL_CSV_2026.splitlines()[:2]
    truncated = iss_row.rsplit(",", 1)[0] + ","

    with pytest.raises(InvalidOrbitMeanElementsError):
        parse_omm_csv(f"{header}\n{truncated}\n")
