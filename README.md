# Tennis Court Finder CLI

Scrape available tennis courts in London from [courtfinder.app](https://www.courtfinder.app/) with distance, time, and day filters.

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python -m tennis_court_scraper
```

## Filters

**Centers** - Default: Angel and Canary Wharf stations. Courts must be within the radius of ALL centers.

```bash
--center 51.5322,-0.0835 --center 51.5054,-0.0205
```

**Radius** - Max distance in km from all centers. Default: 8km.

```bash
--radius 5
```

**Time** - Hour range (0-23). Default: 8-12 (morning slots).

```bash
--start 9 --end 17
```

**Days** - Look-ahead window. Default: 14 days.

```bash
--days-ahead 7
```

**Day of week** - Default: weekends only.

```bash
--weekdays-only
--all-days
```

**Court type**

```bash
--outdoor
--indoor
```

## Example

```bash
uv run python -m tennis_court_scraper --all-days --start 8 --end 20 --radius 5
```
