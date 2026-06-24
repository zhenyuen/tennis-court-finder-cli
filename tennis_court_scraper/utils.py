from collections import defaultdict
from datetime import datetime

from rich.console import Console

from tennis_court_scraper.constants import DATE_FORMAT, MINUTES_PER_HOUR
from tennis_court_scraper.models import Slot

console = Console()


def sort_slots(slots: list[Slot]) -> list[Slot]:
    return sorted(
        slots,
        key=lambda s: (
            datetime.strptime(s.date, DATE_FORMAT),
            s.distance_km,
            s.start_minute,
        ),
    )


def print_slots(slots: list[Slot]) -> None:
    if not slots:
        console.print("[yellow]No matching courts found.[/yellow]")
        return
    grouped: defaultdict[str, list[Slot]] = defaultdict(list)
    for slot in slots:
        grouped[slot.date].append(slot)
    total = 0
    for date_str in sorted(grouped):
        day_slots = grouped[date_str]
        dt = datetime.strptime(date_str, DATE_FORMAT)
        day_name = dt.strftime("%A")
        console.print(f"\n[dim]{date_str} ({day_name})[/dim]  {len(day_slots)} courts")
        for slot in day_slots:
            start_h, start_m = divmod(slot.start_minute, MINUTES_PER_HOUR)
            end_m = start_m + slot.duration_minutes
            end_h = start_h + end_m // MINUTES_PER_HOUR
            end_m = end_m % MINUTES_PER_HOUR
            time_str = f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}"
            price_str = f"[bold]£{slot.price:.2f}[/bold]" if slot.price is not None else "[dim]Free[/dim]"
            outdoor_str = "outdoor" if slot.outdoor else "indoor"
            lit_str = "[green]lit[/green]" if slot.lit else "no lit"
            url_str = f" [dim][link={slot.booking_url}][slot.booking_url][/link][/dim]" if slot.booking_url else ""
            console.print(f"  [cyan]{slot.venue_name}[/cyan] ({slot.venue_id}) [dim]{slot.court_name}[/dim]  {time_str}  {outdoor_str}  {lit_str:<6s}  {price_str}  {slot.distance_km}km{url_str}")
            total += 1
    console.print(f"\n[dim]Total: {total} courts found[/dim]")