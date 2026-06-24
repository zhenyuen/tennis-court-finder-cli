import aiohttp

from tennis_court_scraper.config import (
    COURTFINDER_URL,
)

_REQUEST_TIMEOUT_SECONDS = 30
_REQUEST_USER_AGENT = "TennisCourtScraper/1.0"


async def fetch_html() -> str:
    """Fetch raw HTML from courtfinder.app"""
    timeout = aiohttp.ClientTimeout(total=_REQUEST_TIMEOUT_SECONDS)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(
            COURTFINDER_URL,
            headers={"User-Agent": _REQUEST_USER_AGENT},
        ) as response:
            response.raise_for_status()
            return await response.text()
