""" 
Job Scraper Script

Description:
A modular and efficient job scraper that collects job listings from a website
and saves them in structured format. The script is designed to be scalable,
robust, and easily configurable.

Features:
- Uses requests and BeautifulSoup for web scraping
- Configurable search query and number of pages
- Cleanly structured using functions
- Implements logging for better debugging and transparency
- Handles exceptions gracefully
- Saves data to CSV file
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from types import SimpleNamespace

# --------------------------------------------------
# Configuration Section
# --------------------------------------------------
BASE_URL = "https://www.indeed.com/jobs"
SEARCH_QUERY = "python developer"
LOCATION = "remote"
MAX_PAGES = 5
OUTPUT_FILE = "job_listings.csv"
DELAY = 2  # base seconds delay between requests
DELAY_JITTER = 1.5  # add random jitter
DEBUG_SAVE_DIR = "debug_responses"

# Set up logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure debug directory exists
os.makedirs(DEBUG_SAVE_DIR, exist_ok=True)

# create a requests session with retry/backoff
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount("http://", HTTPAdapter(max_retries=retries))

# small pool of realistic user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

DEFAULT_BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def _get_headers():
    ua = random.choice(USER_AGENTS)
    headers = DEFAULT_BASE_HEADERS.copy()
    headers["User-Agent"] = ua
    return headers

# read optional proxies from environment (useful if you add a proxy later)
PROXIES = None
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if http_proxy or https_proxy:
    PROXIES = {}
    if http_proxy:
        PROXIES["http"] = http_proxy
    if https_proxy:
        PROXIES["https"] = https_proxy

def _playwright_fetch(url: str, headful: bool = False, timeout: int = 30000) -> SimpleNamespace:
    """Fallback: use Playwright to fetch page content. Returns SimpleNamespace(text=html)."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        logging.debug("Playwright not available or failed import: %s", e)
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not headful)
            context = browser.new_context(
                user_agent=_get_headers()["User-Agent"],
                locale="en-US"
            )
            page = context.new_page()
            page.goto(url, timeout=timeout, wait_until="networkidle")
            content = page.content()
            browser.close()
            return SimpleNamespace(text=content)
    except Exception as e:
        logging.debug("Playwright fetch failed for %s: %s", url, e)
        return None

def fetch_page(url: str) -> requests.Response:
    """Fetches a web page using session; on repeated 403 optionally falls back to Playwright.
    Returns a requests.Response or an object with .text attribute (SimpleNamespace) or None.
    """
    max_attempts = 3
    last_status = None
    for attempt in range(1, max_attempts + 1):
        headers = _get_headers()
        try:
            resp = session.get(url, headers=headers, timeout=15, proxies=PROXIES)
            last_status = resp.status_code

            if resp.status_code == 403:
                logging.error("Error fetching URL: %s | HTTP 403 | Forbidden", url)
                try:
                    filename = os.path.join(DEBUG_SAVE_DIR, f"blocked_403_{int(time.time())}.html")
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(resp.text or "")
                    logging.debug("Saved debug response to %s", filename)
                except Exception:
                    logging.debug("Could not save debug response for %s", url)

                backoff = (2 ** (attempt - 1)) + random.random()
                logging.info("Backoff %.1fs before retry %d/%d", backoff, attempt, max_attempts)
                time.sleep(backoff)
                continue

            resp.raise_for_status()
            return resp

        except requests.exceptions.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            logging.error("Error fetching URL: %s | HTTP %s | Exception: %s", url, status, e)
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching URL: %s | Exception: %s", url, e)

        if attempt < max_attempts:
            wait = (2 ** (attempt - 1)) + random.random()
            logging.info("Waiting %.1fs before next attempt for %s", wait, url)
            time.sleep(wait)

    # after retries: if 403 or persistent failure, try Playwright fallback
    if last_status == 403 or os.environ.get("FORCE_PLAYWRIGHT_FALLBACK") == "1":
        logging.info("Attempting Playwright fallback for %s", url)
        pw_resp = _playwright_fetch(url, headful=os.environ.get("PLAYWRIGHT_HEADFUL") == "1")
        if pw_resp:
            logging.info("Playwright fetch succeeded for %s", url)
            return pw_resp

    logging.warning("All fetch attempts failed for %s", url)
    return None


def parse_jobs(html_content: str) -> list:
    """Extracts job details from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    job_cards = soup.find_all('div', class_='job_seen_beacon')

    jobs = []
    for card in job_cards:
        title = card.find('h2', class_='jobTitle')
        company = card.find('span', class_='companyName')
        location = card.find('div', class_='companyLocation')
        summary = card.find('div', class_='job-snippet')

        job_data = {
            "Title": title.text.strip() if title else None,
            "Company": company.text.strip() if company else None,
            "Location": location.text.strip() if location else None,
            "Summary": summary.text.strip() if summary else None
        }
        jobs.append(job_data)

    logging.info(f"Extracted {len(jobs)} jobs from the current page.")
    return jobs


def scrape_jobs(query: str, location: str, pages: int) -> list:
    """Main scraper function that iterates through multiple pages."""
    all_jobs = []
    for page in range(0, pages):
        start = page * 10
        url = f"{BASE_URL}?q={query.replace(' ', '+')}&l={location}&start={start}"
        logging.info(f"Scraping page {page + 1}: {url}")

        response = fetch_page(url)
        if response:
            jobs = parse_jobs(response.text)
            all_jobs.extend(jobs)
        else:
            logging.warning(f"Skipping page {page + 1} due to fetch error.")

        # randomized delay to reduce detection
        sleep_time = DELAY + random.random() * DELAY_JITTER
        time.sleep(sleep_time)

    return all_jobs


def save_to_csv(jobs: list, filename: str):
    """Saves job data to a CSV file."""
    if not jobs:
        logging.warning("No jobs found to save.")
        return

    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    logging.info(f"Saved {len(jobs)} job listings to {filename}.")

if __name__ == "__main__":
    logging.info("Job scraper started.")
    jobs = scrape_jobs(SEARCH_QUERY, LOCATION, MAX_PAGES)
    save_to_csv(jobs, OUTPUT_FILE)
    logging.info("Job scraper finished. Saved results to %s", OUTPUT_FILE)

