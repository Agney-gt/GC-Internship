import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def google_search(query, max_results=10):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    try:
        driver.get("https://www.google.com/")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow time for results to load

        results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

        search_results = []
        for result in results[:max_results]:
            title = result.find_element(By.CSS_SELECTOR, "h3").text
            link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            search_results.append((title, link))

        return search_results

    finally:
        driver.quit()


if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = google_search(query)

    for idx, (title, link) in enumerate(results, start=1):
        print(f"{idx}. {title}\n{link}\n")
