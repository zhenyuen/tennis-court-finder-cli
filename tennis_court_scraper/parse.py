import re

from tennis_court_scraper.models import Slot

_SLOT_REGEX = re.compile(
    r'venueId\\":\\"([A-Z]+)\\",'
    r'\\"courtName\\":\\"([^\\"]+)\\",'
    r'\\"localDate\\":\\"([^\\"]+)\\",'
    r'\\"localStartMinute\\":(\d+),'
    r'\\"durationMinutes\\":(\d+),'
    r'\\"lit\\":(true|false),'
    r'\\"fullSize\\":(true|false),'
    r'\\"outdoor\\":(true|false)'
    r'(?:,\\"price\\":([\d.]+))?'
    r'(?:,\\"outgoingUrl\\":\\"([^\\"]+)\\")?'
)


def parse_slots(html: str) -> list[Slot]:
    """Extract slot records from courtfinder.app HTML"""
    slots = []
    seen = set()
    for match in _SLOT_REGEX.finditer(html):
        venue_id = match.group(1)
        court_name = match.group(2)
        date = match.group(3)
        start_minute = int(match.group(4))
        duration = int(match.group(5))
        lit = match.group(6) == "true"
        full_size = match.group(7) == "true"
        outdoor = match.group(8) == "true"
        price_str = match.group(9)
        price = float(price_str) if price_str and price_str != "0" else None
        booking_url = match.group(10) or ""
        dedup_key = (venue_id, court_name, date, start_minute, duration)
        if dedup_key not in seen:
            seen.add(dedup_key)
            slots.append(Slot(
                venue_id=venue_id,
                court_name=court_name,
                date=date,
                start_minute=start_minute,
                duration_minutes=duration,
                lit=lit,
                full_size=full_size,
                outdoor=outdoor,
                price=price,
                booking_url=booking_url,
            ))
    return slots
