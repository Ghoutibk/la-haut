import pytest

from la_haut.domain.orbit_mean_elements import InvalidOrbitMeanElementsError, OrbitMeanElements
from la_haut.domain.satellite import Satellite
from tests.support.builders import some_orbit_mean_elements
from tests.support.fixtures import ISS_2026_OMM


def test_a_norad_number_beyond_99999_is_read():
    assert some_orbit_mean_elements(NORAD_CAT_ID="100615").norad_id == 100615


def test_the_launch_is_the_year_and_number_of_the_designator_as_in_a_tle():
    assert some_orbit_mean_elements(OBJECT_ID="2026-219B").launch == "26219"


def test_every_piece_of_a_launch_shares_its_launch():
    first = some_orbit_mean_elements(OBJECT_ID="2026-219A")
    later = some_orbit_mean_elements(OBJECT_ID="2026-219BC")

    assert first.launch == later.launch


def test_an_object_without_international_designator_has_no_known_launch():
    assert some_orbit_mean_elements(OBJECT_ID="").launch == ""


@pytest.mark.parametrize("missing", ["EPOCH", "MEAN_MOTION", "NORAD_CAT_ID", "BSTAR"])
def test_elements_missing_a_field_are_rejected(missing):
    fields = {name: value for name, value in ISS_2026_OMM.items() if name != missing}

    with pytest.raises(InvalidOrbitMeanElementsError):
        OrbitMeanElements.from_fields(fields)


@pytest.mark.parametrize(
    "field, value",
    [("MEAN_MOTION", "quinze"), ("NORAD_CAT_ID", "25544.5"), ("EPOCH", "2026-10-06")],
)
def test_elements_with_an_unreadable_value_are_rejected(field, value):
    with pytest.raises(InvalidOrbitMeanElementsError):
        some_orbit_mean_elements(**{field: value})


def test_the_elements_give_back_their_fields_as_published_without_the_name():
    fields = OrbitMeanElements.from_fields(ISS_2026_OMM).as_fields()

    assert fields == {name: value for name, value in ISS_2026_OMM.items() if name != "OBJECT_NAME"}


def test_a_satellite_can_be_known_by_its_orbit_mean_elements():
    satellite = Satellite(
        name="STARLINK-38345", elements=some_orbit_mean_elements(NORAD_CAT_ID="100615")
    )

    assert satellite.norad_id == 100615
