import time
import csv
from typing import List, Dict, Any
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

SearchResult = Dict[str, str]

def generate_filename(query: str) -> str:
    sanitized_query = re.sub(r'[^a-zA-Z0-9\s]+', '', query).strip()
    safe_query = sanitized_query.replace(' ', '_')[:30].lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if safe_query:
        return f"google_results_{safe_query}_{timestamp}.csv"
    else:
        return f"google_results_empty_query_{timestamp}.csv"

def configure_browser() -> Options:
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    return chrome_options

def extract_search_results(driver: webdriver.Chrome) -> List[SearchResult]:
    print("[INFO] Attempting to extract search snippets...")
    time.sleep(3)
    all_results: List[SearchResult] = []
    result_containers = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
    for container in result_containers:
        try:
            title_element = container.find_element(By.TAG_NAME, "h3")
            title = title_element.text
            link_element = container.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")
            desc_elements = container.find_elements(By.CSS_SELECTOR, "div.VwiC3b")
            description = desc_elements[0].text if desc_elements else "No summary available"
            all_results.append({
                "Title": title,
                "Description": description,
                "Link": link
            })
        except NoSuchElementException:
            print("[WARNING] Skipped a result block due to missing elements.")
            continue
        except Exception as e:
            print(f"[ERROR] Failed to process a result: {e}")
            continue
    return all_results

def save_to_csv(results: List[SearchResult], filename: str = "google_search_results.csv"):
    if not results:
        print("[WARNING] No data to save.")
        return
    fieldnames = list(results[0].keys())
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"[SUCCESS] Successfully saved {len(results)} results to {filename}")
    except Exception as e:
        print(f"[ERROR] Could not write CSV file: {e}")

def run_search_scraper(query: str):
    print(f"\n--- Starting Google Search for: '{query}' ---")
    options = configure_browser()
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com/")
        time.sleep(2)
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        print("[INFO] Waiting for search results to load...")
        time.sleep(4)
        search_data = extract_search_results(driver)
        dynamic_filename = generate_filename(query)
        save_to_csv(search_data, filename=dynamic_filename)
    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected error occurred during execution: {e}")
        if driver:
            driver.save_screenshot("error_screenshot.png")
            print("[INFO] Saved 'error_screenshot.png' for inspection.")
    finally:
        if driver:
            driver.quit()
            print("[INFO] Browser closed successfully.")
        print("\n--- Process Finished ---")

if __name__ == "__main__":
    search_term = input("What would you like to search for on Google? ")
    if search_term.strip():
        run_search_scraper(search_term)
    else:
        print("Search term cannot be empty. Exiting.")
