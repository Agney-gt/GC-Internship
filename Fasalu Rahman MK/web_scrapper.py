from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
def scrape_google_results(query, num_results=10):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(20) # adjust to solve captcha 
        results = []
        search_results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']")
        for result in search_results[:num_results]:
            try:
                title = result.find_element(By.XPATH, ".//h3").text
                link = result.find_element(By.XPATH, ".//a").get_attribute("href")
                results.append({"title": title, "link": link})
            except Exception as e:
                print(f"Error scraping a result: {e}")

        return results

    finally:
        driver.quit()
if __name__ == "__main__":
    query = input("Enter your search query: ")
    num_results = int(input("Enter the number of results to scrape: "))
    results = scrape_google_results(query, num_results)
    for i, result in enumerate(results, start=1):
        print(f"Result {i}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print("-")
