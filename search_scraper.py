import sys
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

def build_driver(headless: bool = False, window_size: str = "1200,800"):
    opts = Options()
    if headless:
        # headless can sometimes be blocked; run non-headless for reliability in interviews
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={window_size}")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # set a common user-agent (optional)
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    return driver

def scrape_google(query: str, num_results: int = 10, headless: bool = False, pause: float = 1.0) -> List[Dict]:
    driver = build_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    results = []
    try:
        driver.get("https://www.google.com")
        # Accept cookies if shown (simple attempt)
        try:
            consent = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Agree')]")))
            consent.click()
            time.sleep(0.5)
        except Exception:
            pass

        # Search
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        time.sleep(pause)

        # Google markup changes. Use multiple heuristics for result blocks.
        # Primary: div#search div.g (common)
        blocks = driver.find_elements(By.CSS_SELECTOR, "div#search div.g")
        if not blocks:
            # fallback: search for css that often wraps results
            blocks = driver.find_elements(By.CSS_SELECTOR, "div#search .tF2Cxc")

        count = 0
        for b in blocks:
            if count >= num_results:
                break
            try:
                # Title
                title_el = None
                try:
                    title_el = b.find_element(By.CSS_SELECTOR, "h3")
                except NoSuchElementException:
                    pass

                # Link (anchor)
                link_el = None
                try:
                    link_el = b.find_element(By.CSS_SELECTOR, "a")
                except NoSuchElementException:
                    pass

                # Snippet
                snippet_el = None
                snippet_selectors = ["div.IsZvec", "div.VwiC3b", "div.st", "span.aCOpRe"]  # various old/new selectors
                for sel in snippet_selectors:
                    try:
                        snippet_el = b.find_element(By.CSS_SELECTOR, sel)
                        break
                    except NoSuchElementException:
                        snippet_el = None

                title = title_el.text.strip() if title_el else ""
                url = link_el.get_attribute("href") if link_el else ""
                snippet = snippet_el.text.strip() if snippet_el else ""

                # Skip empty results (ads or widgets) without useful data
                if not title and not url:
                    continue

                results.append({"title": title, "url": url, "snippet": snippet})
                count += 1
            except Exception:
                # don't crash on one bad block, move on
                continue

        # If not enough results from initial page, optionally go to next page (not implemented by default)
    finally:
        driver.quit()
    return results

def main():
    parser = argparse.ArgumentParser(description="Simple Selenium Google search scraper")
    parser.add_argument("query", type=str, help="Search query (wrap in quotes)")
    parser.add_argument("--num", type=int, default=10, help="Number of results to return")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    args = parser.parse_args()

    out = scrape_google(args.query, num_results=args.num, headless=args.headless)
    for i, r in enumerate(out, 1):
        print(f"{i}. {r['title']}")
        print(f"   URL: {r['url']}")
        if r['snippet']:
            print(f"   Snippet: {r['snippet']}")
        print("")

if __name__ == "__main__":
    main()