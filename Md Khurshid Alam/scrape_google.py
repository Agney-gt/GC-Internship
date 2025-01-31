from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options (optional: run in headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in the background without opening a browser window

# Set up the WebDriver (ensure the correct driver is installed and in your PATH)
service = Service(executable_path="/path/to/chromedriver")  # Replace with the path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box and enter a query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python Selenium scraping")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load (better to use WebDriverWait instead of time.sleep)
    time.sleep(3)  # Temporary solution; replace with WebDriverWait for better practice

    # Scrape the search results
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    for index, result in enumerate(results, start=1):
        print(f"Result {index}: {result.text}")

finally:
    # Close the browser
    driver.quit()