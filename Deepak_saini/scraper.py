from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#Setup webdrive:
driver = webdriver.Firefox()

#Open Google:
driver.get("https://www.google.com/ncr")

#find the Search box and enter the query:
text_box = driver.find_element(By.NAME, "q")
text_box.send_keys("Internship opportunities")
text_box.send_keys(Keys.RETURN)

#wait for result to load
time.sleep(3)

results = driver.find_elements(By.CSS_SELECTOR, "h3")

print(results)
for result in results:
    print(result.text)
driver.quit()

