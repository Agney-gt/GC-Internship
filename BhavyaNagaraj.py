from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Change the path if necessary)
driver = webdriver.Chrome()  # or webdriver.Firefox()

# Open Google
driver.get("https://www.google.com")

# Find the search box and enter a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python tutorial")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(3)

# Extract search result titles
results = driver.find_elements(By.CSS_SELECTOR, "h3")

print("Top Google Search Results:")
for index, result in enumerate(results[:5]):  # Get top 5 results
    print(f"{index+1}. {result.text}")

# Close the browser
driver.quit()
