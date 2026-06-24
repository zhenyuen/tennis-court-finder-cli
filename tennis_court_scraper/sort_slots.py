from datetime import datetime

from tennis_court_scraper.constants import DATE_FORMAT
from tennis_court_scraper.models import Slot


def sort_slots(slots: list[Slot]) -> list[Slot]:
    return sorted(
        slots,
        key=lambda s: (
            datetime.strptime(s.date, DATE_FORMAT),
            s.distance_km,
            s.start_minute,
        ),
    )
