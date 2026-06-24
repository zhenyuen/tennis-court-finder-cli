from datetime import datetime

from tennis_court_scraper.constants import DATE_FORMAT
from tennis_court_scraper.models import Slot

_WEEKEND_START = 5


def filter_by_day_of_week(
    slots: list[Slot],
    weekends_only: bool = True,
    weekdays_only: bool = False,
) -> list[Slot]:
    if not weekends_only and not weekdays_only:
        return slots
    result: list[Slot] = []
    for slot in slots:
        dow = datetime.strptime(slot.date, DATE_FORMAT).weekday()
        is_weekend = dow >= _WEEKEND_START
        is_weekday = dow < _WEEKEND_START
        if (weekends_only and is_weekend) or (weekdays_only and is_weekday):
            result.append(slot)
    return result
