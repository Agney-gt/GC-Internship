# scraper.py
# Author: Ritesh Rathod
# Task: Selenium-based Google Search Scraper
# Internship: GC Internship 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def google_search_scraper(query):

    chrome_options = Options()
    chrome_options.add_argument("--headless")       # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service() 

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(2)  # Wait for results to load

        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")

        print(f"\n Top Google search results for: '{query}'\n")

        for i, result in enumerate(results[:10], 1):
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.get_attribute("href")
            print(f"{i}. {title}\n   {link}\n")

    except Exception as e:
        print(" Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    # You can change this query or take input from user
    query = input("Enter a search term: ") or "latest technology news"
    google_search_scraper(query)
