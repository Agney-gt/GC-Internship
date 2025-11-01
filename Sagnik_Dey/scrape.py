import argparse
import csv
import json
import os
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# WebDriver setup
def build_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# Accept cookies / consent
def accept_consent(driver):
    buttons = [
        (By.ID, "L2AGLb"),
        (By.XPATH, "//button//div[text()='I agree']/.."),
        (By.XPATH, "//button//span[contains(text(),'Accept')]/.."),
    ]
    for by, sel in buttons:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
            btn.click()
            time.sleep(0.5)
            return
        except Exception:
            continue


# Extract search results
def extract_results(driver) -> List[Dict[str, str]]:
    results = []
    selectors = ["div.tF2Cxc", "div.MjjYud", "div.g"]

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
        )
    except TimeoutException:
        return results

    blocks = []
    for sel in selectors:
        blocks.extend(driver.find_elements(By.CSS_SELECTOR, sel))

    for block in blocks:
        try:
            title_el = block.find_element(By.CSS_SELECTOR, "h3")
            link_el = block.find_element(By.XPATH, ".//a[.//h3]")
            snippet_el = None
            for s in ["div.VwiC3b", "span.aCOpRe", "div[data-sncf='1']"]:
                els = block.find_elements(By.CSS_SELECTOR, s)
                if els:
                    snippet_el = els[0]
                    break

            title = title_el.text.strip()
            link = link_el.get_attribute("href") or ""
            snippet = snippet_el.text.strip() if snippet_el else ""

            if title and link.startswith("http"):
                results.append({"title": title, "snippet": snippet, "link": link})
        except Exception:
            continue
    return results


# Scroll down to load results
def scroll_to_load(driver, scrolls=2):
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(scrolls):
        body.send_keys(Keys.END)
        time.sleep(2)


# Save to JSON and CSV
def save_results(results, query):
    # Ensure 'results' directory exists
    os.makedirs("results", exist_ok=True)

    # Clean up query name for filenames
    base_name = query.replace(" ", "_")
    json_file = os.path.join("results", f"{base_name}_results.json")
    csv_file = os.path.join("results", f"{base_name}_results.csv")

    # Save as JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save as CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "snippet", "link"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to 'results/' folder:\n - {json_file}\n - {csv_file}")


# Core scraper
def scrape_google(query, limit=10, headless=False, lang="en"):
    driver = build_driver(headless)
    results = []
    try:
        url = (
            f"https://www.google.com/search?q={query.replace(' ', '+')}&hl={lang}&pws=0"
        )
        print(f"[INFO] Searching Google for: '{query}' ...")
        driver.get(url)
        time.sleep(2)
        accept_consent(driver)

        scroll_to_load(driver, 2)
        new_results = extract_results(driver)
        results.extend(new_results[:limit])

        print(f"[INFO] Extracted {len(results)} results.")
        return results
    finally:
        driver.quit()


# CLI entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape Google Search results using Selenium."
    )
    parser.add_argument("--query", "-q", required=True, help="Search query string")
    parser.add_argument(
        "--limit", "-n", type=int, default=10, help="Number of results to extract"
    )
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    parser.add_argument(
        "--lang", default="en", help="Google interface language, e.g., en, en-IN"
    )
    args = parser.parse_args()

    results = scrape_google(args.query, args.limit, args.headless, args.lang)
    if not results:
        print("No results found or Google layout changed.")
    else:
        save_results(results, args.query)
