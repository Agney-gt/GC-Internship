from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver
service = Service("C:\Windows\chromedriver.exe")  
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to Google
    driver.get("https://www.google.com")

    # Find the search box
    search_box = driver.find_element(By.NAME, "q")

    # Enter the search query
    search_query = "Selenium Python"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(2)

    # Extract search results
    results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')

    # Print the titles and URLs of the first 5 results
    for result in results[:5]:
        title = result.find_element(By.TAG_NAME, 'h3').text
        url = result.get_attribute('href')
        print(f"Title: {title}\nURL: {url}\n")

finally:
    # Close the browser
    driver.quit()
