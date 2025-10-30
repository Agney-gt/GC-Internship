# google_scraper.py
# Author: Samridhi
# Description: This script uses Selenium to scrape Google search results and display the top 10 titles.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_google_results(query):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open Google
        driver.get("https://www.google.com")
        time.sleep(2)

        # Find the search box
        search_box = driver.find_element(By.NAME, "q")

        # Enter the search query
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results
        time.sleep(3)

        # Fetch top results
        results = driver.find_elements(By.CSS_SELECTOR, "h3")

        print(f"\n🔍 Top Google search results for: '{query}'\n")
        for i, result in enumerate(results[:10], start=1):
            print(f"{i}. {result.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

# ---- Run the function ----
if __name__ == "__main__":
    query = input("Enter your search query: ")
    scrape_google_results(query)
