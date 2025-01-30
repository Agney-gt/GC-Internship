import os
import sys
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

def scrape_google_results(query, num_results=10):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")   # Suppresses warning to keep console clean
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Apply stealth
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to load or for CAPTCHA
    try:
        print("Waiting for search results to load...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tF2Cxc')))
        print("Search results loaded.")
    except Exception as e:
        print("Error loading search results or CAPTCHA required:", e)
        driver.quit()
        return []

    time.sleep(random.uniform(3, 6))  # Random sleep to mimic human behavior

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
        except Exception as e:
            print("Error parsing result:", e)  # Log parsing errors

    driver.quit()
    return results

# Function to save data to CSV
def save_to_csv(data, filename='google_results.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Description"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_data = scrape_google_results(search_query)

    if scraped_data:
        save_to_csv(scraped_data)
    else:
        print("No results found.")