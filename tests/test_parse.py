from tennis_court_scraper.parse import parse_slots


SAMPLE_HTML = """
<div>
  {"venueId\\":\\"ABTS\\",\\"courtName\\":\\"Court 1\\",\\"localDate\\":\\"2026-06-27\\",\\"localStartMinute\\":480,\\"durationMinutes\\":60,\\"lit\\":true,\\"fullSize\\":true,\\"outdoor\\":true,\\"price\\":8.0,\\"outgoingUrl\\":\\"https://example.com/book\\"}
  {"venueId\\":\\"ABTS\\",\\"courtName\\":\\"Court 1\\",\\"localDate\\":\\"2026-06-27\\",\\"localStartMinute\\":480,\\"durationMinutes\\":60,\\"lit\\":true,\\"fullSize\\":true,\\"outdoor\\":true,\\"price\\":8.0,\\"outgoingUrl\\":\\"https://example.com/book\\"}
  {"venueId\\":\\"BRIT\\",\\"courtName\\":\\"Indoor Court\\",\\"localDate\\":\\"2026-06-28\\",\\"localStartMinute\\":600,\\"durationMinutes\\":90,\\"lit\\":true,\\"fullSize\\":true,\\"outdoor\\":false,\\"price\\":12.50,\\"outgoingUrl\\":\\"https://example.com/2\\"}
  {"venueId\\":\\"HILL\\",\\"courtName\\":\\"Park Court\\",\\"localDate\\":\\"2026-06-27\\",\\"localStartMinute\\":360,\\"durationMinutes\\":60,\\"lit\\":false,\\"fullSize\\":true,\\"outdoor\\":true}
</div>
"""


def test_parse_extracts_slots():
    slots = parse_slots(SAMPLE_HTML)
    assert len(slots) == 3


def test_parse_deduplicates():
    slots = parse_slots(SAMPLE_HTML)
    venue_ids = [s.venue_id for s in slots]
    assert venue_ids.count("ABTS") == 1


def test_parse_fields():
    slots = parse_slots(SAMPLE_HTML)
    abts = next(s for s in slots if s.venue_id == "ABTS")
    assert abts.court_name == "Court 1"
    assert abts.date == "2026-06-27"
    assert abts.start_minute == 480
    assert abts.duration_minutes == 60
    assert abts.lit is True
    assert abts.full_size is True
    assert abts.outdoor is True
    assert abts.price == 8.0
    assert abts.booking_url == "https://example.com/book"


def test_parse_no_price():
    slots = parse_slots(SAMPLE_HTML)
    hill = next(s for s in slots if s.venue_id == "HILL")
    assert hill.price is None
    assert hill.lit is False
    assert hill.outdoor is True


def test_parse_indoor():
    slots = parse_slots(SAMPLE_HTML)
    brit = next(s for s in slots if s.venue_id == "BRIT")
    assert brit.outdoor is False
    assert brit.price == 12.5


def test_parse_empty_html():
    slots = parse_slots("<div>no slots here</div>")
    assert slots == []
