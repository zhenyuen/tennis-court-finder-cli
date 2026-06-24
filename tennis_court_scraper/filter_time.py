from datetime import UTC, datetime, timedelta

from tennis_court_scraper.constants import DATE_FORMAT, MINUTES_PER_HOUR
from tennis_court_scraper.models import Slot


def filter_by_time(
    slots: list[Slot],
    start_hour: int,
    end_hour: int,
    days_ahead: int,
) -> list[Slot]:
    today = datetime.now(UTC).date()
    cutoff = today + timedelta(days=days_ahead)
    result: list[Slot] = []
    for slot in slots:
        slot_date = datetime.strptime(slot.date, DATE_FORMAT).date()
        start_hour_val = slot.start_minute // MINUTES_PER_HOUR
        if slot_date < today or slot_date >= cutoff:
            continue
        if start_hour_val < start_hour or start_hour_val >= end_hour:
            continue
        result.append(slot)
    return result
