from tennis_court_scraper.models import Slot


def test_slot_defaults():
    slot = Slot(
        venue_id="ABTS",
        court_name="Court 1",
        date="2026-06-25",
        start_minute=480,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=True,
        price=8.0,
        booking_url="https://example.com",
    )
    assert slot.venue_name == ""
    assert slot.distance_km == 0.0


def test_slot_no_price():
    slot = Slot(
        venue_id="ABTS",
        court_name="Court 1",
        date="2026-06-25",
        start_minute=480,
        duration_minutes=60,
        lit=False,
        full_size=False,
        outdoor=False,
        price=None,
        booking_url="",
    )
    assert slot.price is None


def test_slot_set_distance():
    slot = Slot(
        venue_id="ABTS",
        court_name="Court 1",
        date="2026-06-25",
        start_minute=480,
        duration_minutes=60,
        lit=True,
        full_size=True,
        outdoor=True,
        price=8.0,
        booking_url="",
    )
    slot.distance_km = 3.5
    slot.venue_name = "Test Venue"
    assert slot.distance_km == 3.5
    assert slot.venue_name == "Test Venue"
