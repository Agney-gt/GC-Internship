from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

try:
    # Set up ChromeDriver
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in your PATH

    # Go to Google
    driver.get("https://www.google.com")

    # Find the search box and input a search query
    search_box = driver.find_element("name", "q")
    search_box.send_keys("Selenium Python tutorial")
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(1000)

    # Scrape the titles of the search results
    results = driver.find_elements("css selector", "h3")
    for result in results:
        print(result.text)

except Exception as e:
    print("Error:", e)

finally:
    # Close the browser
    driver.quit()
