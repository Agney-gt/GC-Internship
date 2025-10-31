import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def google_search(query, max_results=5, driver_path=None, headless=True):
    if driver_path is None:
        raise ValueError("Please set driver_path to your chromedriver executable")

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com/")
        time.sleep(2)  

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query + Keys.RETURN)
        time.sleep(2)  

        results = []
        anchors = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        for a in anchors[:max_results]:
            title = a.find_element(By.TAG_NAME, "h3").text
            url = a.get_attribute("href")
            results.append({"title": title, "url": url})

        return results

    finally:
        driver.quit()

def main():
    query = input("Enter search query: ").strip()
    max_results = 5
    driver_path = "/path/to/chromedriver"
    try:
        data = google_search(query, max_results=max_results, driver_path=driver_path, headless=True)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    print(f"Top {len(data)} results for \"{query}\":\n")
    for idx, item in enumerate(data, start=1):
        print(f"{idx}. {item['title']}")
        print(f"   {item['url']}")
        print()

if __name__ == "__main__":
    main()
