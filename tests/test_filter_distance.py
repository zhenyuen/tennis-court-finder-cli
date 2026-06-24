from tennis_court_scraper.filters import filter_by_distance
from tennis_court_scraper.models import Slot


def _make_slot(venue_id: str) -> Slot:
    return Slot(
        venue_id=venue_id,
        court_name="Court",
        date="2026-06-27",
        start_minute=480,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=True,
        price=8.0,
        booking_url="",
    )


def test_filter_within_radius():
    slots = [
        _make_slot("BRIT"),
        _make_slot("HILL"),
    ]
    angel = (51.5322, -0.0835)
    result = filter_by_distance(slots, [angel], 8.0)
    assert len(result) == 2
    for s in result:
        assert s.distance_km <= 8.0


def test_filter_excludes_far():
    slots = [_make_slot("CARL")]
    angel = (51.5322, -0.0835)
    result = filter_by_distance(slots, [angel], 2.0)
    assert len(result) == 0


def test_filter_intersection():
    slots = [_make_slot("BRIT")]
    angel = (51.5322, -0.0835)
    canary = (51.5054, -0.0205)
    result = filter_by_distance(slots, [angel, canary], 8.0)
    assert len(result) == 1
    assert result[0].distance_km <= 8.0


def test_filter_sets_venue_name():
    slots = [_make_slot("BRIT")]
    result = filter_by_distance(slots, [(51.5322, -0.0835)], 8.0)
    assert result[0].venue_name == "Britannia Leisure Centre"


def test_filter_unknown_venue():
    slots = [_make_slot("ZZZZ")]
    result = filter_by_distance(slots, [(51.5322, -0.0835)], 8.0)
    assert len(result) == 1
    assert "Unknown" in result[0].venue_name


def test_filter_multiple_centers():
    slots = [_make_slot("HILL")]
    angel = (51.5322, -0.0835)
    canary = (51.5054, -0.0205)
    result = filter_by_distance(slots, [angel, canary], 8.0)
    assert len(result) == 1
