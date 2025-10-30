from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_once(query, wait_time=15):
    """Open browser, search query on DuckDuckGo, print top results, then close browser."""
    driver = webdriver.Chrome()
    try:
        driver.get("https://duckduckgo.com")

        search = driver.find_element(By.NAME, "q")
        search.send_keys(query)
        search.send_keys(Keys.RETURN)

        WebDriverWait(driver, wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']"))
        )

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        titles = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        print(f"\nTop Search Results for: {query}\n")
        for i, title in enumerate(titles[:10], start=1):
            print(f"{i}. {title.text}\n   {title.get_attribute('href')}\n")

    except Exception as e:
        print("Timeout or no results:", e)
    finally:
        driver.quit()   

if __name__ == "__main__":
    print("Type your search and press Enter. Type 'exit' to quit.")
    while True:
        q = input("\nEnter search (or 'exit'): ").strip()
        if not q:
            print("Please enter a search term or 'exit'.")
            continue
        if q.lower() == "exit":
            print("Goodbye.")
            break

        search_once(q)
