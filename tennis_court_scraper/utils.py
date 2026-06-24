from collections import defaultdict
from datetime import datetime

from rich.console import Console
from rich.table import Table

from tennis_court_scraper.constants import DATE_FORMAT, MINUTES_PER_HOUR
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


def _format_time(slot: Slot) -> str:
    start_h, start_m = divmod(slot.start_minute, MINUTES_PER_HOUR)
    end_m = start_m + slot.duration_minutes
    end_h = start_h + end_m // MINUTES_PER_HOUR
    end_m = end_m % MINUTES_PER_HOUR
    return f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}"


def print_slots(slots: list[Slot], plain: bool = False) -> None:
    console = Console(no_color=plain, width=10000 if plain else None)

    if not slots:
        console.print("No matching courts found." if plain else "[yellow]No matching courts found.[/yellow]")
        return

    grouped: defaultdict[str, list[Slot]] = defaultdict(list)
    for slot in slots:
        grouped[slot.date].append(slot)

    total = 0
    for date_str in sorted(grouped):
        day_slots = grouped[date_str]
        dt = datetime.strptime(date_str, DATE_FORMAT)
        day_name = dt.strftime("%A")
        console.print(f"\n{date_str} ({day_name})  {len(day_slots)} courts")

        table = Table(
            show_header=True,
            header_style="bold" if not plain else "none",
            box=None,
            padding=(0, 1),
        )
        table.add_column("Venue", style="cyan" if not plain else "none")
        table.add_column("Court")
        table.add_column("Time")
        table.add_column("Type")
        table.add_column("Size")
        table.add_column("Light")
        table.add_column("Price")
        table.add_column("Max Dist (Angel/CW)")
        table.add_column("URL", overflow="fold")

        for slot in day_slots:
            time_str = _format_time(slot)
            price_str = f"£{slot.price:.2f}" if slot.price is not None else "Free"
            outdoor_str = "outdoor" if slot.outdoor else "indoor"
            lit_str = "lit" if slot.lit else "no lit"
            size_str = "full" if slot.full_size else "half"
            url_str = slot.booking_url if plain else (f"[link={slot.booking_url}]book[/link]" if slot.booking_url else "")

            table.add_row(
                f"{slot.venue_name} ({slot.venue_id})",
                slot.court_name,
                time_str,
                outdoor_str,
                size_str,
                lit_str,
                price_str,
                f"{slot.distance_km}km",
                url_str,
            )
            total += 1

        console.print(table)

    console.print(f"\nTotal: {total} courts found")