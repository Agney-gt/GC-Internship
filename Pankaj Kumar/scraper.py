#!/usr/bin/env python3
"""
Google Search Scraper (Stealth + DuckDuckGo Fallback)

Description:
    A professional Selenium-based web scraper with stealth mode and a fallback
    to DuckDuckGo if Google blocks the search due to CAPTCHA or rate limiting.

Features:
    - Stealth-enabled browser (selenium-stealth)
    - Detects and handles CAPTCHA gracefully
    - Falls back to DuckDuckGo to ensure results always appear
    - Headless / visible mode options
    - Random user-agent rotation and human-like delays
    - Saves output to CSV and JSON with UTF-8 encoding
    - Command-line interface for flexible use

Setup:
    pip install selenium webdriver-manager selenium-stealth

Usage:
    python scraper.py "AI automation" --results 10 --csv results.csv --headless
"""

import csv
import json
import random
import time
from typing import List, Optional
from urllib.parse import urlparse, parse_qs, quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


# ---------------- Utility Functions ---------------- #

def extract_domain(url: str) -> str:
    """Extracts domain name from a given URL."""
    try:
        return urlparse(url).netloc
    except Exception:
        return ""


def extract_actual_url(href: str) -> str:
    """Unwraps Google's redirect links like /url?q=..."""
    if not href:
        return ""
    if "/url?" in href or "google.com/url" in href:
        try:
            parsed = urlparse(href)
            q = parse_qs(parsed.query).get("q")
            if q:
                return q[0]
        except Exception:
            return href
    return href


# ---------------- Main Scraper Class ---------------- #

class GoogleScraper:
    def __init__(self, headless: bool = True, delay_range=(2.0, 4.0)):
        self.headless = headless
        self.min_delay, self.max_delay = delay_range
        self.driver = None
        self.wait = None
        self._start_driver()

    def _start_driver(self):
        """Initializes Chrome WebDriver with stealth and anti-detection options."""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1200,800")
        options.add_argument("--lang=en-US")

        # Random user-agent rotation
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

        # Apply stealth
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

    def close(self):
        """Safely closes WebDriver."""
        try:
            if self.driver:
                self.driver.quit()
        except Exception:
            pass

    def _get_search_url(self, query: str, start: int = 0) -> str:
        """Builds a proper Google search URL."""
        return f"https://www.google.com/search?q={quote_plus(query)}&hl=en&num=100&start={start}"

    def _page_has_captcha(self) -> bool:
        """Detects if Google has blocked the scraper."""
        src = (self.driver.page_source or "").lower()
        return any(keyword in src for keyword in [
            "unusual traffic", "are you a robot", "complete the captcha"
        ])

    def load_page(self, query: str, start: int = 0):
        """Loads the search results page."""
        url = self._get_search_url(query, start)
        self.driver.get(url)
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "search")))
        except Exception:
            pass
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def parse_results(self, start_offset=0) -> List[dict]:
        """Extracts search results (title, URL, snippet) from the current page."""
        results = []
        try:
            root = self.driver.find_element(By.ID, "search")
        except Exception:
            return results

        containers = root.find_elements(By.CSS_SELECTOR, "div.tF2Cxc, div.g, div.MjjYud")
        pos = start_offset

        for g in containers:
            try:
                h3 = g.find_element(By.TAG_NAME, "h3")
                title = h3.text.strip()
                if not title:
                    continue

                href = ""
                try:
                    a_tag = g.find_element(By.CSS_SELECTOR, "a")
                    href = a_tag.get_attribute("href")
                except Exception:
                    continue

                url = extract_actual_url(href)
                if not url or "googleadservices" in url:
                    continue

                snippet = ""
                for sel in ["div.IsZvec", "div.VwiC3b", "span.aCOpRe"]:
                    try:
                        snippet = g.find_element(By.CSS_SELECTOR, sel).text.strip()
                        if snippet:
                            break
                    except Exception:
                        continue

                pos += 1
                results.append({
                    "position": pos,
                    "title": title,
                    "url": url,
                    "domain": extract_domain(url),
                    "snippet": snippet
                })

            except Exception:
                continue

        return results

    # ---------------- DuckDuckGo Fallback ---------------- #
    def duckduckgo_fallback(self, query: str, num_results=10) -> List[dict]:
        """Fallback search using DuckDuckGo."""
        print("[INFO] Switching to DuckDuckGo fallback...")

        fallback_results = []
        try:
            url = f"https://duckduckgo.com/?q={quote_plus(query)}"
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".result__title")))
            time.sleep(random.uniform(2, 4))

            items = self.driver.find_elements(By.CSS_SELECTOR, ".result__title")[:num_results]
            for i, item in enumerate(items, 1):
                try:
                    a_tag = item.find_element(By.TAG_NAME, "a")
                    title = a_tag.text.strip()
                    link = a_tag.get_attribute("href")
                    fallback_results.append({
                        "position": i,
                        "title": title,
                        "url": link,
                        "domain": extract_domain(link),
                        "snippet": ""
                    })
                except Exception:
                    continue
        except Exception as e:
            print("[ERROR] Fallback search failed:", e)

        return fallback_results

    def run(self, query: str, num_results=10, csv_path="results.csv", json_path=None):
        """Main execution flow."""
        print(f"[INFO] Searching for: {query}")
        start_time = time.time()
        self.load_page(query)

        # CAPTCHA Handling
        if self._page_has_captcha():
            print("[ERROR] CAPTCHA or unusual traffic detected. Saving page...")
            with open("captcha_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            # Attempt DuckDuckGo fallback
            results = self.duckduckgo_fallback(query, num_results)
            self.save_results(results, csv_path, json_path)
            self.close()
            return results

        data = self.parse_results()
        if not data:
            print("[WARN] No results found.")
            data = self.duckduckgo_fallback(query, num_results)

        data = data[:num_results]
        self.save_results(data, csv_path, json_path)

        duration = time.time() - start_time
        print(f"[INFO] Completed scraping {len(data)} results in {duration:.2f} seconds.")
        self.close()
        return data

    def save_results(self, data: List[dict], csv_path: Optional[str] = None, json_path: Optional[str] = None):
        """Saves scraped results to CSV and optionally JSON."""
        if not data:
            print("[INFO] No data to save.")
            return

        keys = ["position", "title", "url", "domain", "snippet"]
        if csv_path:
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"[INFO] Saved {len(data)} results to {csv_path}")

        if json_path:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] Saved JSON: {json_path}")


# ---------------- CLI Entry Point ---------------- #

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Google + DuckDuckGo Stealth Search Scraper")
    parser.add_argument("query", help="Search query (in quotes)")
    parser.add_argument("--results", type=int, default=10, help="Number of results to fetch")
    parser.add_argument("--csv", default="results.csv", help="CSV output path")
    parser.add_argument("--json", default=None, help="Optional JSON output path")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")

    args = parser.parse_args()

    scraper = GoogleScraper(headless=args.headless)
    scraper.run(args.query, num_results=args.results, csv_path=args.csv, json_path=args.json)
