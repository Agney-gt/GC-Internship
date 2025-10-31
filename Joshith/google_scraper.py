from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def google_search(query):
    print(f"\n🔍 Searching Google for: {query}\n")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get("https://www.google.com/")
        time.sleep(2)
        
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()

        print("[INFO] Loading results, please wait...")
        time.sleep(3)

        results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

        scraped_data = []

        for result in results:
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                description_element = result.find_elements(By.CSS_SELECTOR, "div.VwiC3b")
                description = description_element[0].text if description_element else "No description"

                scraped_data.append([title, description, link])
            except Exception:
                continue

        if scraped_data:
            file_name = f"google_results_{query.replace(' ', '_')}.csv"
            with open(file_name, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Description", "Link"])
                writer.writerows(scraped_data)
            print(f"[SUCCESS] {len(scraped_data)} results saved to '{file_name}'.")
        else:
            print("[WARNING] No results found or page layout changed.")

    except Exception as e:
        print(f"[ERROR] Something went wrong: {e}")

    finally:
        driver.quit()
        print("[INFO] Browser closed successfully.")

if __name__ == "__main__":
    print("=== Google Search Scraper ===")
    keyword = input("Enter a topic to search: ").strip()
    if keyword:
        google_search(keyword)
    else:
        print("No keyword entered. Exiting...")
