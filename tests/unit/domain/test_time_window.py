from datetime import datetime, timedelta

import pytest

from la_haut.domain.time_window import InvalidTimeWindowError, TimeWindow
from tests.support.builders import DEFAULT_INSTANT


def test_a_window_spans_from_its_start_to_its_end():
    window = TimeWindow(starts_at=DEFAULT_INSTANT, ends_at=DEFAULT_INSTANT + timedelta(hours=8))

    assert window.duration == timedelta(hours=8)


def test_a_window_must_end_after_it_starts():
    with pytest.raises(InvalidTimeWindowError):
        TimeWindow(starts_at=DEFAULT_INSTANT, ends_at=DEFAULT_INSTANT)


def test_a_window_requires_timezone_aware_instants():
    with pytest.raises(InvalidTimeWindowError):
        TimeWindow(starts_at=datetime(2026, 10, 5, 18), ends_at=datetime(2026, 10, 6, 6))
