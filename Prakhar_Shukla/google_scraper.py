import time
import csv
import re
import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

SearchResult = Dict[str, str]


def sanitize_filename(query: str) -> str:
    """Generate a clean, timestamped filename."""
    clean_query = re.sub(r"[^a-zA-Z0-9\s]+", "", query).strip().replace(" ", "_").lower()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{clean_query or 'google_search'}_{timestamp}.csv"



def setup_browser(headless: bool = False) -> webdriver.Chrome:
    """Configure Chrome browser with custom options."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    # 🧠 Custom user-agent to mimic real Chrome browser
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def extract_results(driver: webdriver.Chrome) -> List[SearchResult]:
    """Extract search results from the Google results page."""
    print("[INFO] Extracting search results...")
    results: List[SearchResult] = []
    containers = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc") or driver.find_elements(By.CSS_SELECTOR, "div.g")

    for c in containers:
        try:
            title_elem = c.find_element(By.TAG_NAME, "h3")
            link_elem = c.find_element(By.TAG_NAME, "a")
            desc_elem = c.find_elements(By.CSS_SELECTOR, "div.VwiC3b")
            results.append(
                {
                    "Title": title_elem.text.strip(),
                    "Description": desc_elem[0].text.strip() if desc_elem else "No description",
                    "Link": link_elem.get_attribute("href"),
                }
            )
        except Exception:
            continue

    print(f"[INFO] Extracted {len(results)} results.")
    return results


def scroll_to_bottom(driver, scroll_pause: float = 1.5, max_scrolls: int = 3):
    """Scrolls down to load more search results."""
    print("[INFO] Scrolling to load more results...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("[INFO] Scrolling complete.")


def save_results_to_csv(results: List[SearchResult], filename: str):
    """Save extracted results to a CSV file."""
    if not results:
        print("[WARNING] No results to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"[SUCCESS] Saved {len(results)} results to '{filename}'")


def google_search(query: str, headless: bool):
    """Perform a Google search and extract top results."""
    print(f"\n🔍 Searching Google for: {query}\n")
    driver = None

    try:
        driver = setup_browser(headless=headless)
        driver.get("https://www.google.com/")

        # Accept consent popup if present
        try:
            consent = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='Accept']"))
            )
            consent.click()
            print("[INFO] Accepted Google consent.")
        except TimeoutException:
            pass

        # Type the query and search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.submit()

        print("[INFO] Waiting for results to appear...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tF2Cxc"))
            )
        except TimeoutException:
            print("[WARN] Results took too long; continuing anyway...")

        scroll_to_bottom(driver)
        results = extract_results(driver)
        filename = sanitize_filename(query)
        save_results_to_csv(results, filename)

    except WebDriverException as e:
        print(f"[ERROR] Browser issue: {e}")
    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
    finally:
        if driver:
            driver.quit()
        print("[INFO] Browser closed.\n--- Process Completed ---")


if __name__ == "__main__":
    print("=== Google Search Scraper ===")
    query = input("Enter your Google search query: ").strip()
    if not query:
        print("Search query cannot be empty. Exiting.")
        exit()

    headless_input = input("Run in headless mode? (y/n): ").strip().lower()
    headless_mode = headless_input == "y"

    google_search(query, headless=headless_mode)
