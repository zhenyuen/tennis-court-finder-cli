import pytest

from tennis_court_scraper.fetch import fetch_html


@pytest.mark.asyncio
async def test_fetch_returns_html():
    html = await fetch_html()
    assert isinstance(html, str)
    assert len(html) > 100000


@pytest.mark.asyncio
async def test_fetch_contains_slots():
    html = await fetch_html()
    assert 'venueId\\":\\"' in html


@pytest.mark.asyncio
async def test_fetch_follows_redirects():
    html = await fetch_html()
    assert "<html" in html.lower() or "<!DOCTYPE" in html.upper()
