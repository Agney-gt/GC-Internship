"""
Google Search Results Scraper
Contributor: Paridhi Nagori
Description:
This script automates a Google search with Selenium, extracts the titles and URLs of the first N results,
and writes them to a CSV file. Ideal for demonstrating web automation and scraping basics.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import time
import os
import sys

def configure_driver(headless: bool = True):
    """Configures the Chrome WebDriver with options."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Using Selenium Manager to manage driver automatically
    driver = webdriver.Chrome(options=options)
    return driver

def perform_search(driver, query: str, timeout: int = 10):
    """Performs Google search for the given query and returns list of result elements."""
    driver.get("https://www.google.com")
    # Wait for search box to appear
    wait = WebDriverWait(driver, timeout)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(query + Keys.RETURN)
    # Wait for search results container
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    # Collect result containers
    result_elements = driver.find_elements(By.XPATH, '//div[@class="tF2Cxc"]')
    return result_elements

def extract_results(result_elements, max_results: int = 10):
    """Extracts title and URL from each result element up to max_results."""
    data = []
    for idx, elem in enumerate(result_elements[:max_results], start=1):
        try:
            title_elem = elem.find_element(By.TAG_NAME, "h3")
            link_elem = elem.find_element(By.TAG_NAME, "a")
            title = title_elem.text.strip()
            url = link_elem.get_attribute("href").strip()
            data.append({"Rank": idx, "Title": title, "URL": url})
        except Exception as e:
            print(f"[WARN] Could not extract element #{idx} due to {e}", file=sys.stderr)
    return data

def save_as_csv(data, filename: str = "google_search_results.csv"):
    """Saves the list of dictionaries into a CSV file."""
    if not data:
        print("[INFO] No data to save.")
        return
    headers = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"[SUCCESS] Data saved to {filename}")

def main():`
    query = input("Enter search query: ").strip()
    if not query:
        print("No query entered, exiting.")
        return

    driver = None
    try:
        driver = configure_driver(headless=True)
        results = perform_search(driver, query)
        extracted = extract_results(results, max_results=10)
        for r in extracted:
            print(f"{r['Rank']}. {r['Title']}\n   {r['URL']}")
        save_as_csv(extracted)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
