from tennis_court_scraper.filter_time import filter_by_time
from tennis_court_scraper.models import Slot


def _make_slot(date: str, start_minute: int) -> Slot:
    return Slot(
        venue_id="ABTS",
        court_name="Court",
        date=date,
        start_minute=start_minute,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=True,
        price=8.0,
        booking_url="",
    )


def test_filter_within_hours():
    slots = [
        _make_slot("2026-06-27", 480),
        _make_slot("2026-06-27", 540),
    ]
    result = filter_by_time(slots, 8, 12, 14)
    assert len(result) == 2


def test_filter_excludes_early():
    slots = [_make_slot("2026-06-27", 300)]
    result = filter_by_time(slots, 8, 12, 14)
    assert len(result) == 0


def test_filter_excludes_late():
    slots = [_make_slot("2026-06-27", 780)]
    result = filter_by_time(slots, 8, 12, 14)
    assert len(result) == 0


def test_filter_excludes_past():
    slots = [_make_slot("2020-01-01", 480)]
    result = filter_by_time(slots, 8, 12, 14)
    assert len(result) == 0


def test_filter_excludes_far_future():
    slots = [_make_slot("2030-01-01", 480)]
    result = filter_by_time(slots, 8, 12, 14)
    assert len(result) == 0
