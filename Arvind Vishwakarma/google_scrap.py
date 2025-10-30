from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scrape_google(query, num_results=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.google.com")

    # Search
    box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    box.send_keys(query + Keys.RETURN)

    # Wait for results
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
    )

    results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
    data = []

    for r in results[:num_results]:
        title = r.text
        url = r.get_attribute("href")
        data.append({"title": title, "url": url})

    driver.quit()
    return data


if __name__ == "__main__":
    keyword = input("Search: ")
    output = scrape_google(keyword, num_results=5)

    print("\nTop Results:\n")
    for item in output:
        print(item["title"], " --> ", item["url"])
