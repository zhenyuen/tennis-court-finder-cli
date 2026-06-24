from datetime import datetime

from tennis_court_scraper.models import Slot


def filter_by_day_of_week(
    slots: list[Slot],
    weekends_only: bool = True,
    weekdays_only: bool = False,
) -> list[Slot]:
    if not weekends_only and not weekdays_only:
        return slots
    result: list[Slot] = []
    for slot in slots:
        dow = datetime.strptime(slot.date, "%Y-%m-%d").weekday()
        is_weekend = dow >= 5
        is_weekday = dow < 5
        if (weekends_only and is_weekend) or (weekdays_only and is_weekday):
            result.append(slot)
    return result
