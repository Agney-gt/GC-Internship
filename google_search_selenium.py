"""
google_search_selenium.py
Simple Selenium script that performs a Google search and extracts result titles and URLs.

Usage:
    python google_search_selenium.py "search query" 10

Notes:
 - Uses webdriver-manager to auto-install the ChromeDriver.
 - Uses explicit waits to be more robust.
 - Respect robots and rate limits when scraping in bulk.
"""

import sys
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def fetch_google_results(query: str, max_results: int = 10, headless: bool = True) -> List[Dict]:
    # Setup Chrome
    options = Options()
    if headless:
        # modern Chrome prefers --headless=new, but fallback to --headless works too
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")
    # Optional: set a reasonable window size so elements render like a real browser
    options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # Build URL and load
        q = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={q}&num={min(max_results, 100)}"
        driver.get(url)

        # Wait until results container loads
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#search")))

        results = []
        # Each standard search result is within div#search .g — there are also other blocks; this is robust for classic results
        items = driver.find_elements(By.CSS_SELECTOR, "div#search .g")
        for item in items:
            if len(results) >= max_results:
                break
            try:
                a = item.find_element(By.CSS_SELECTOR, "a")
                title_el = item.find_element(By.CSS_SELECTOR, "h3")
                href = a.get_attribute("href")
                title = title_el.text.strip()
                if title and href:
                    results.append({"title": title, "url": href})
            except Exception:
                # skip items that are not standard results (ads, knowledge panels, etc.)
                continue

        return results

    finally:
        driver.quit()


def main():
    if len(sys.argv) < 2:
        print("Usage: python google_search_selenium.py \"search query\" [max_results]")
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    print(f"Searching Google for: {query} (max {max_results})")
    results = fetch_google_results(query, max_results=max_results, headless=True)

    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print()

    print(f"Total results scraped: {len(results)}")


if __name__ == "__main__":
    main()
