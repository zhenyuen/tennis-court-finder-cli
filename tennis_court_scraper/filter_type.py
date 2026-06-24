from tennis_court_scraper.models import Slot


def filter_by_type(
    slots: list[Slot],
    outdoor_only: bool = False,
    indoor_only: bool = False,
) -> list[Slot]:
    if not outdoor_only and not indoor_only:
        return slots
    result: list[Slot] = []
    for slot in slots:
        if outdoor_only and slot.outdoor:
            result.append(slot)
        elif indoor_only and not slot.outdoor:
            result.append(slot)
    return result
