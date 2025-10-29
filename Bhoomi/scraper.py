from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.google.com")
search_box = driver.find_element("name", "q")
search_box.send_keys("OpenAI ChatGPT")
search_box.send_keys(Keys.RETURN)

results = driver.find_elements("tag name", "h3")
for result in results:
    print(result.text)

driver.quit()
