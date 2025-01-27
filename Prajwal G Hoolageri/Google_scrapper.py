import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def scrape_google_results(query, num_results=10):
    # Setup Selenium WebDriver with stealth
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    driver.get("https://www.google.com")

    # Perform search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    print("Solve the CAPTCHA if prompted. Waiting for search results to load...")

    # Wait for CAPTCHA to be solved and results to load
    while True:
        if len(driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")) > 0:
            print("CAPTCHA solved, proceeding...")
            break
        time.sleep(5)  # Check every 5 seconds

    # Scrape results
    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")

    for result in search_results[:num_results]:
        try:
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            snippet = result.find_element(By.CSS_SELECTOR, ".VwiC3b").text

            print(f"Title: {title}")
            results.append({"Title": title, "Link": link, "Description": snippet})
        except Exception:
            continue

    driver.quit()
    return results

def save_to_json(data, filename='google_results.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_data = scrape_google_results(search_query)

    if scraped_data:
        save_to_json(scraped_data)
    else:
        print("No results found.")
