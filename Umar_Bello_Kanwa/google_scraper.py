from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

search_query = "your-query"

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")

    # Increase tiem if it takes more to load
    time.sleep(2)

    # Locate the search bar
    search_box = driver.find_element(By.NAME, "q")

    # Enter the search query and press Enter
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Scrape the search results
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
    for idx, result in enumerate(search_results, start=1):
        title = result.find_element(By.TAG_NAME, "h3").text
        link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        snippet = result.find_element(By.CSS_SELECTOR, ".VwiC3b").text
        print(f"Result {idx}:\nTitle: {title}\nLink: {link}\nSnippet: {snippet}\n")

finally:
    driver.quit()