from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_google(query):
    driver=webdriver.Chrome()
    driver.get("https://www.google.com")
    search_box=driver.find_element(By.NAME,"q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(50)

    results=driver.find_elements(By.CSS_SELECTOR,"div.yuRUbf a")
    for i, r in enumerate(results[:10],start=1):
        print(f"{i}.{r.text}-{r.get_attribute('href')}")

    driver.quit()

if __name__=="__main__":
    search_google("Selenium Python tutorial")
