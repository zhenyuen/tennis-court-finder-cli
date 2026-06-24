import argparse
import asyncio
import sys

import aiohttp

from tennis_court_scraper.config import (
    DEFAULT_CENTERS,
    DEFAULT_DAYS_AHEAD,
    DEFAULT_END_HOUR,
    DEFAULT_RADIUS_KM,
    DEFAULT_START_HOUR,
)
from tennis_court_scraper.fetch import fetch_html
from tennis_court_scraper.filter_dayofweek import filter_by_day_of_week
from tennis_court_scraper.filter_distance import filter_by_distance
from tennis_court_scraper.filter_time import filter_by_time
from tennis_court_scraper.filter_type import filter_by_type
from tennis_court_scraper.parse import parse_slots
from tennis_court_scraper.utils import print_slots, sort_slots

COURTFINDER_MAX_DAYS_AHEAD = 9


def _parse_center(value: str) -> tuple[float, float]:
    lat, lng = value.split(",")
    return (float(lat), float(lng))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find available tennis courts near you")
    parser.add_argument(
        "--center",
        action="append",
        default=[f"{lat},{lng}" for lat, lng in DEFAULT_CENTERS],
        metavar="LAT,LNG",
        help="Center point(s) to filter by. Can be repeated. Default: Angel + Canary Wharf",
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=DEFAULT_RADIUS_KM,
        help=f"Maximum distance in km from all centers. Default: {DEFAULT_RADIUS_KM}",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=DEFAULT_START_HOUR,
        help=f"Earliest start hour (0-23). Default: {DEFAULT_START_HOUR}",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=DEFAULT_END_HOUR,
        help=f"Latest start hour (0-23). Default: {DEFAULT_END_HOUR}",
    )
    parser.add_argument(
        "--days-ahead",
        type=int,
        default=DEFAULT_DAYS_AHEAD,
        help=f"Number of days to look ahead. Default: {DEFAULT_DAYS_AHEAD}",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--weekends-only",
        action="store_true",
        default=True,
        help="Show weekends only (default)",
    )
    group.add_argument(
        "--weekdays-only",
        action="store_true",
        default=False,
        help="Show weekdays only",
    )
    group.add_argument(
        "--all-days",
        action="store_true",
        default=False,
        help="Show all days",
    )
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        "--outdoor",
        action="store_true",
        help="Outdoor courts only",
    )
    type_group.add_argument(
        "--indoor",
        action="store_true",
        help="Indoor courts only",
    )
    return parser


async def run() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.days_ahead > COURTFINDER_MAX_DAYS_AHEAD:
        print(
            "Warning: courtfinder.app only provides %s days of data ahead"
            % COURTFINDER_MAX_DAYS_AHEAD,
            file=sys.stderr,
        )
    centers = [_parse_center(c) for c in args.center]
    try:
        html = await fetch_html()
    except aiohttp.ClientError as e:
        print("Error fetching data: %s" % e, file=sys.stderr)
        sys.exit(1)
    slots = parse_slots(html)
    slots = filter_by_distance(slots, centers, args.radius)
    slots = filter_by_time(slots, args.start, args.end, args.days_ahead)
    weekends_only = not args.weekdays_only and not args.all_days
    weekdays_only = args.weekdays_only
    slots = filter_by_day_of_week(slots, weekends_only, weekdays_only)
    slots = filter_by_type(slots, args.outdoor, args.indoor)
    slots = sort_slots(slots)
    print_slots(slots)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
