
from tennis_court_scraper.utils import print_slots
from tennis_court_scraper.models import Slot


def _make_slot(date: str, start_minute: int, distance: float, outdoor: bool = True, price: float | None = 8.0, lit: bool = True, venue_name: str = "Test Venue") -> Slot:
    return Slot(
        venue_id="ABTS",
        court_name="Court",
        date=date,
        start_minute=start_minute,
        duration_minutes=60,
        lit=lit,
        full_size=True,
        outdoor=outdoor,
        price=price,
        booking_url="",
        venue_name=venue_name,
        distance_km=distance,
    )


def test_print_no_slots(capsys):
    print_slots([])
    captured = capsys.readouterr()
    assert "No matching courts found" in captured.out


def test_print_with_slots(capsys):
    slots = [
        _make_slot("2026-06-27", 480, 2.0),
        _make_slot("2026-06-27", 540, 3.0),
    ]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "2026-06-27" in captured.out
    assert "Saturday" in captured.out
    assert "2 courts" in captured.out
    assert "Total: 2 courts found" in captured.out


def test_print_time_format(capsys):
    slots = [_make_slot("2026-06-27", 480, 2.0)]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "08:00-09:00" in captured.out


def test_print_price(capsys):
    slots = [_make_slot("2026-06-27", 480, 2.0, price=8.0)]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "£8.00" in captured.out


def test_print_free(capsys):
    slots = [_make_slot("2026-06-27", 480, 2.0, price=None)]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "Free" in captured.out


def test_print_outdoor_indoor(capsys):
    slots = [
        _make_slot("2026-06-27", 480, 2.0, outdoor=True),
        _make_slot("2026-06-27", 540, 2.0, outdoor=False),
    ]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "outdoor" in captured.out
    assert "indoor" in captured.out


def test_print_distance(capsys):
    slots = [_make_slot("2026-06-27", 480, 3.5)]
    print_slots(slots)
    captured = capsys.readouterr()
    assert "3.5km" in captured.out
