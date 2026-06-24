from collections import defaultdict
from datetime import datetime

from tennis_court_scraper.models import Slot


def print_slots(slots: list[Slot]) -> None:
    if not slots:
        print("No matching courts found.")
        return
    grouped: defaultdict[str, list[Slot]] = defaultdict(list)
    for slot in slots:
        grouped[slot.date].append(slot)
    total = 0
    for date_str in sorted(grouped):
        day_slots = grouped[date_str]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = dt.strftime("%A")
        print(f"\n{date_str} ({day_name})  {len(day_slots)} courts")
        for slot in day_slots:
            start_h, start_m = divmod(slot.start_minute, 60)
            end_m = start_m + slot.duration_minutes
            end_h = start_h + end_m // 60
            end_m = end_m % 60
            time_str = f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}"
            price_str = f"£{slot.price:.2f}" if slot.price is not None else "Free"
            outdoor_str = "outdoor" if slot.outdoor else "indoor"
            lit_str = "lit" if slot.lit else "no lit"
            print(f"  {slot.venue_name} ({slot.venue_id:4s})  {time_str}  {outdoor_str}  {lit_str:<6s}  {price_str}  {slot.distance_km}km")
            total += 1
    print(f"\nTotal: {total} courts found")
