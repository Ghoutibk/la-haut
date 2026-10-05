import pytest

from la_haut.domain.observer import InvalidObserverError, Observer


def test_an_observer_stands_at_a_latitude_and_longitude():
    paris = Observer(latitude_deg=48.8566, longitude_deg=2.3522)

    assert (paris.latitude_deg, paris.longitude_deg, paris.altitude_m) == (48.8566, 2.3522, 0.0)


@pytest.mark.parametrize("latitude_deg", [-90.01, 90.01])
def test_an_observer_cannot_stand_beyond_the_poles(latitude_deg):
    with pytest.raises(InvalidObserverError):
        Observer(latitude_deg=latitude_deg, longitude_deg=0.0)


@pytest.mark.parametrize("longitude_deg", [-180.01, 180.01])
def test_an_observer_longitude_stays_within_minus_180_to_180_degrees(longitude_deg):
    with pytest.raises(InvalidObserverError):
        Observer(latitude_deg=0.0, longitude_deg=longitude_deg)
