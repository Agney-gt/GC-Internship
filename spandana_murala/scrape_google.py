from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python tutorial")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    print("Top search results:")
    for index, result in enumerate(results[:5], 1):
        print(f"{index}. {result.text}")
finally:
    driver.quit()
##END##s
