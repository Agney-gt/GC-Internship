from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

query = "Amazon brands advertising"

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Google
driver.get("https://www.google.com")
time.sleep(2)

# Find search box
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)

time.sleep(3)

# Collect all search results (titles + links)
results = driver.find_elements(By.CSS_SELECTOR, "div.g")

print("\n=== GOOGLE RESULTS ===\n")

for result in results:
    try:
        title = result.find_element(By.TAG_NAME, "h3").text
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(f"{title} → {link}")
    except:
        continue

driver.quit()
