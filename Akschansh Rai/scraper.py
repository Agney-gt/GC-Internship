# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def google_search(query, num_results=10):
    options = uc.ChromeOptions()
    options.add_argument("--headless")  
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = uc.Chrome(options=options)
    
    driver.get("https://www.google.com")
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)
    
    results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")[:num_results]
    
    search_results = []
    for result in results:
        title = result.find_element(By.CSS_SELECTOR, "h3").text
        link = result.find_element(By.CSS_SELECTOR, "div.yuRUbf a").get_attribute("href")
        search_results.append((title, link))
    
    driver.quit()
    
    return search_results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = google_search(query)
    
    for idx, (title, link) in enumerate(results, start=1):
        print(f"{idx}. {title}\n   {link}\n")
