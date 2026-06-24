from tennis_court_scraper.filters import filter_by_day_of_week
from tennis_court_scraper.models import Slot


def _make_slot(date: str) -> Slot:
    return Slot(
        venue_id="ABTS",
        court_name="Court",
        date=date,
        start_minute=480,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=True,
        price=8.0,
        booking_url="",
    )


def test_filter_weekends_only():
    slots = [
        _make_slot("2026-06-25"),
        _make_slot("2026-06-27"),
        _make_slot("2026-06-28"),
    ]
    result = filter_by_day_of_week(slots, weekends_only=True)
    dates = [s.date for s in result]
    assert "2026-06-25" not in dates
    assert "2026-06-27" in dates
    assert "2026-06-28" in dates


def test_filter_weekdays_only():
    slots = [
        _make_slot("2026-06-25"),
        _make_slot("2026-06-27"),
    ]
    result = filter_by_day_of_week(slots, weekends_only=False, weekdays_only=True)
    dates = [s.date for s in result]
    assert "2026-06-25" in dates
    assert "2026-06-27" not in dates


def test_filter_all_days():
    slots = [
        _make_slot("2026-06-25"),
        _make_slot("2026-06-27"),
    ]
    result = filter_by_day_of_week(slots, weekends_only=False, weekdays_only=False)
    assert len(result) == 2
