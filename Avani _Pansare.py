from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH

try:
    # Open Google
    driver.get("https://www.google.com")

    # Accept cookies if prompted (update selector based on your region)
    try:
        accept_button = driver.find_element(By.XPATH, "//button[text()='Accept all']")
        accept_button.click()
    except:
        pass

    # Search for a query
    search_box = driver.find_element(By.NAME, "q")
    search_query = "Selenium Python tutorial"
    search_box.send_keys(search_query + Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # Scrape search result titles and URLs
    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']")  # Adjust selector if needed

    for idx, result in enumerate(results[:10], start=1):  # Limiting to top 10 results
        title = result.find_element(By.TAG_NAME, "h3").text
        url = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        print(f"{idx}. {title} - {url}")

finally:
    driver.quit()
