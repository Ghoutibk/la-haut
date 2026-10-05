from datetime import timedelta

from la_haut.composition import build_list_visible_passes_from_celestrak
from la_haut.domain.time_window import TimeWindow
from tests.support.builders import an_observer_in_paris
from tests.support.fake_celestrak import FakeCelestrak
from tests.support.fixtures import ISS_NAME, ISS_TLE_EPOCH, ISS_TLE_LINE_1, ISS_TLE_LINE_2


def test_the_brightest_satellites_from_celestrak_are_tracked_over_the_observer(tmp_path):
    day_after_epoch = TimeWindow(starts_at=ISS_TLE_EPOCH, ends_at=ISS_TLE_EPOCH + timedelta(days=1))

    with FakeCelestrak() as celestrak:
        celestrak.publishes(ISS_NAME, ISS_TLE_LINE_1, ISS_TLE_LINE_2)
        list_visible_passes = build_list_visible_passes_from_celestrak(
            tmp_path / "visual.tle", base_url=celestrak.url
        )
        [iss_pass] = list_visible_passes.execute(an_observer_in_paris(), day_after_epoch)

    assert iss_pass.satellite_name == ISS_NAME
