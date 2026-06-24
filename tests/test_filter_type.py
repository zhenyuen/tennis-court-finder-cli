from tennis_court_scraper.filters import filter_by_type
from tennis_court_scraper.models import Slot


def _make_slot(outdoor: bool) -> Slot:
    return Slot(
        venue_id="ABTS",
        court_name="Court",
        date="2026-06-27",
        start_minute=480,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=outdoor,
        price=8.0,
        booking_url="",
    )


def test_filter_outdoor_only():
    slots = [
        _make_slot(outdoor=True),
        _make_slot(outdoor=False),
    ]
    result = filter_by_type(slots, outdoor_only=True)
    assert len(result) == 1
    assert result[0].outdoor is True


def test_filter_indoor_only():
    slots = [
        _make_slot(outdoor=True),
        _make_slot(outdoor=False),
    ]
    result = filter_by_type(slots, indoor_only=True)
    assert len(result) == 1
    assert result[0].outdoor is False


def test_filter_no_preference():
    slots = [
        _make_slot(outdoor=True),
        _make_slot(outdoor=False),
    ]
    result = filter_by_type(slots)
    assert len(result) == 2
