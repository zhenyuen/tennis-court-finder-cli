from tennis_court_scraper.sort_slots import sort_slots
from tennis_court_scraper.models import Slot


def _make_slot(date: str, start_minute: int, distance: float) -> Slot:
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
        distance_km=distance,
    )


def test_sort_by_date():
    slots = [
        _make_slot("2026-06-28", 480, 2.0),
        _make_slot("2026-06-27", 480, 2.0),
    ]
    result = sort_slots(slots)
    assert result[0].date == "2026-06-27"
    assert result[1].date == "2026-06-28"


def test_sort_by_distance_same_date():
    slots = [
        _make_slot("2026-06-27", 480, 5.0),
        _make_slot("2026-06-27", 480, 2.0),
    ]
    result = sort_slots(slots)
    assert result[0].distance_km == 2.0
    assert result[1].distance_km == 5.0


def test_sort_by_time_same_date_distance():
    slots = [
        _make_slot("2026-06-27", 600, 2.0),
        _make_slot("2026-06-27", 480, 2.0),
    ]
    result = sort_slots(slots)
    assert result[0].start_minute == 480
    assert result[1].start_minute == 600


def test_sort_empty():
    result = sort_slots([])
    assert result == []
