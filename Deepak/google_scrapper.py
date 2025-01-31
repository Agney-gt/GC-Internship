import os
import sys
import time
import csv
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Function to initialize WebDriver with necessary options
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # Suppresses warnings to keep console clean
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    # Setup WebDriver and ChromeDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to perform Google search and scrape results
def scrape_google_results(query, num_results=10):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress unnecessary logs to keep console clean

    driver = initialize_driver()

    # Apply stealth to avoid detection
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    # Open Google and perform the search
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for CAPTCHA to be solved by checking if search results appear
    print("Solve the CAPTCHA if prompted. Waiting for search results to load...")
    while True:
        if len(driver.find_elements(By.CSS_SELECTOR, '.tF2Cxc')) > 0:
            print("CAPTCHA solved, proceeding...")
            break
        time.sleep(5)

    # Wait a random time before scraping the results
    time.sleep(random.uniform(3, 6))

    # Scrape the results
    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, '.tF2Cxc')

    for result in search_results[:num_results]:
        try:
            title_element = result.find_element(By.TAG_NAME, "h3")
            link_element = result.find_element(By.CSS_SELECTOR, "a")
            snippet_element = result.find_element(By.CSS_SELECTOR, ".VwiC3b")

            title = title_element.text if title_element else "No Title"
            link = link_element.get_attribute("href") if link_element else "No Link"
            snippet = snippet_element.text if snippet_element else "No Description"

            results.append({
                "Title": title,
                "Link": link,
                "Description": snippet
            })
        except Exception:
            pass  # Suppress parsing errors

    driver.quit()
    return results

# Function to save data to CSV
def save_to_csv(data, filename='google_results.csv'):
    if data:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Description"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Results saved to {filename}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_data = scrape_google_results(search_query)

    if scraped_data:
        save_to_csv(scraped_data)
    else:
        print("No results found.")
