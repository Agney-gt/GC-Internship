from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Make sure you have ChromeDriver installed)
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.google.com")

# Find the search bar and enter a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Web Scraping")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(2)

# Scrape search results
search_results = driver.find_elements(By.CSS_SELECTOR, "h3")

print("Top Google Search Results:")
for index, result in enumerate(search_results[:5], start=1):
    print(f"{index}. {result.text}")

# Close the browser
driver.quit()
