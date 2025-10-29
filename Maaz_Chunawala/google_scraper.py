from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

def scrape_google(query, max_results=10, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com")
        time.sleep(1)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # wait for results

        results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
        output = []
        for idx, result in enumerate(results[:max_results], start=1):
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
            except:
                title = "No title found"
            try:
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "No link found"
            output.append((idx, title, link))

        return output

    finally:
        driver.quit()


if __name__ == "__main__":
    q = "Web development internship"
    results = scrape_google(q, max_results=10, headless=False)
    print(f"Top results for '{q}':\n")
    for idx, title, link in results:
        print(f"{idx}. {title}\n   {link}\n")