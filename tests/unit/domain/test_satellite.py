import pytest

from la_haut.domain.satellite import InvalidTwoLineElementsError, Satellite, TwoLineElements
from tests.support.fixtures import (
    ISS_NAME,
    ISS_TLE_LINE_1,
    ISS_TLE_LINE_2,
    STARLINK_TRAIN,
    STARLINK_TRAIN_LAUNCH,
)

ISS_ELEMENTS = TwoLineElements(ISS_TLE_LINE_1, ISS_TLE_LINE_2)


def test_a_satellite_is_identified_by_the_norad_number_of_its_elements():
    iss = Satellite(name=ISS_NAME, elements=ISS_ELEMENTS)

    assert iss.norad_id == 25544


def test_elements_with_a_wrong_checksum_are_rejected():
    corrupted_line_1 = ISS_TLE_LINE_1[:-1] + "4"

    with pytest.raises(InvalidTwoLineElementsError):
        TwoLineElements(corrupted_line_1, ISS_TLE_LINE_2)


def test_elements_with_a_truncated_line_are_rejected():
    with pytest.raises(InvalidTwoLineElementsError):
        TwoLineElements(ISS_TLE_LINE_1[:60], ISS_TLE_LINE_2)


def test_elements_given_in_the_wrong_order_are_rejected():
    with pytest.raises(InvalidTwoLineElementsError):
        TwoLineElements(ISS_TLE_LINE_2, ISS_TLE_LINE_1)


def test_elements_mixing_two_satellites_are_rejected():
    line_2_of_another_satellite = (
        "2 25545  51.6414 295.8524 0003435 262.6267 204.2868 15.54005638121107"
    )

    with pytest.raises(InvalidTwoLineElementsError):
        TwoLineElements(ISS_TLE_LINE_1, line_2_of_another_satellite)


def test_the_launch_is_read_from_the_international_designator_without_the_piece_letter():
    assert ISS_ELEMENTS.launch == "98067"


def test_satellites_of_the_same_launch_share_it():
    launches = {TwoLineElements(line_1, line_2).launch for _, line_1, line_2 in STARLINK_TRAIN}

    assert launches == {STARLINK_TRAIN_LAUNCH}
