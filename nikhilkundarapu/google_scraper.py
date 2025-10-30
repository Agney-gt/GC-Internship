# google_scraper.py
# Author: Sai Nikhil
# Internship Task: Use Selenium to scrape Google search results

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_google_results(query):
    """Scrapes top Google search result titles for a given query."""
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        print(f"\nTop Google Search Results for '{query}':\n")
        for i, result in enumerate(results[:10], start=1):
            print(f"{i}. {result.text}")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    user_query = input("Enter your Google search query: ")
    scrape_google_results(user_query)