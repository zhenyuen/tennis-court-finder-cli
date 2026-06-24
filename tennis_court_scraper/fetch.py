import httpx

from tennis_court_scraper.config import (
    COURTFINDER_URL,
)

_REQUEST_TIMEOUT_SECONDS = 30
_REQUEST_USER_AGENT = "TennisCourtScraper/1.0"


async def fetch_html() -> str:
    """Fetch raw HTML from courtfinder.app"""
    async with httpx.AsyncClient(timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.get(
            COURTFINDER_URL,
            headers={"User-Agent": _REQUEST_USER_AGENT},
            follow_redirects=True,
        )
        response.raise_for_status()
        return response.text
