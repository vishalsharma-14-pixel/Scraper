import time
from dataclasses import dataclass

import httpx

from app.config import settings
from app.models.snapshot import FetchMethod
from app.services import extractor


class ScraperFetchError(Exception):
    pass


@dataclass
class ScrapeOutcome:
    raw_values: dict[str, str | None]
    fetch_method: FetchMethod


def _fetch_http(url: str) -> str:
    headers = {"User-Agent": settings.default_user_agent}
    last_error: Exception | None = None

    for attempt in range(settings.max_fetch_retries + 1):
        try:
            with httpx.Client(
                timeout=settings.request_timeout_seconds,
                headers=headers,
                follow_redirects=True,
            ) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError) as exc:
            last_error = exc
            if attempt < settings.max_fetch_retries:
                time.sleep(settings.retry_backoff_seconds)

    raise ScraperFetchError(f"HTTP fetch failed for {url}: {last_error}") from last_error


def _fetch_headless(url: str) -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=settings.default_user_agent)
            page.goto(
                url,
                wait_until="networkidle",
                timeout=settings.playwright_nav_timeout_seconds * 1000,
            )
            return page.content()
        finally:
            browser.close()


def fetch_and_extract(tracker) -> ScrapeOutcome:
    config = tracker.extraction_config

    if tracker.requires_js is not True:
        html = _fetch_http(tracker.url)
        raw_values = extractor.extract_fields(html, config)
        if tracker.requires_js is False or not extractor.looks_incomplete(raw_values, config):
            return ScrapeOutcome(raw_values=raw_values, fetch_method=FetchMethod.HTTP)

    html = _fetch_headless(tracker.url)
    raw_values = extractor.extract_fields(html, config)
    return ScrapeOutcome(raw_values=raw_values, fetch_method=FetchMethod.HEADLESS)
