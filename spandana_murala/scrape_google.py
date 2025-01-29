from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
d = webdriver.Chrome()

try:
    d.get("https://www.google.com")
    search_box = d.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python tutorial")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    results = d.find_elements(By.CSS_SELECTOR, "h3")
    print("Top search results:")
    for index, result in enumerate(results[:5], 1):
        print(f"{index}. {result.text}")
finally:
    d.quit()
##END##s
