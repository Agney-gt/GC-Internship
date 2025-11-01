from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import csv
import json
import sys


class GoogleScraper:
    """A class to scrape Google search results using Selenium."""

    def __init__(self, headless=True, service_path="chromedriver", user_agent=None):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--start-maximized')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument(
            f'user-agent={user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}')
        self.service = Service(service_path)
        self.driver = None
        self.results = []

    def start_driver(self):
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("[INFO] Chrome WebDriver started.")
        except Exception as e:
            print(f"[ERROR] Unable to start WebDriver: {e}")
            sys.exit(1)

    def search_google(self, query, num_results=10, delay=2):
        if not self.driver:
            self.start_driver()
        try:
            self.driver.get("https://www.google.com")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search")))
            time.sleep(delay)
            self.results = self._extract_results(num_results)
            print(f"[INFO] Scraped {len(self.results)} results.")
            return self.results
        except Exception as e:
            print(f"[ERROR] Google search failed: {e}")
            return []

    def _extract_results(self, num_results):
        results = []
        try:
            # Find all result containers
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            for index, result in enumerate(search_results[:num_results], 1):
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text or "N/A"
                    url = result.find_element(By.TAG_NAME, "a").get_attribute("href") or "N/A"
                    description = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text if result.find_elements(By.CSS_SELECTOR, "div.VwiC3b") else "N/A"
                    results.append({
                        'rank': index,
                        'title': title,
                        'url': url,
                        'description': description
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"[ERROR] Extraction of results failed: {e}")
        return results

    def save_to_csv(self, filename):
        if not self.results:
            print("[WARN] No results to save.")
            return
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['rank', 'title', 'url', 'description'])
                writer.writeheader()
                writer.writerows(self.results)
            print(f"[INFO] Saved results to '{filename}'")
        except Exception as e:
            print(f"[ERROR] Could not save CSV: {e}")

    def save_to_json(self, filename):
        if not self.results:
            print("[WARN] No results to save.")
            return
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.results, file, indent=4, ensure_ascii=False)
            print(f"[INFO] Saved results to '{filename}'")
        except Exception as e:
            print(f"[ERROR] Could not save JSON: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()
            print("[INFO] WebDriver closed.")


def main():
    scraper = GoogleScraper(headless=True)
    try:
        query = input("Enter search query: ")
        num_results = int(input("How many results? (default=10): ") or "10")
        results = scraper.search_google(query, num_results)
        print("\n" + "="*80)
        print("SEARCH RESULTS")
        print("="*80 + "\n")
        for result in results:
            print(f"Rank: {result['rank']}")
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Description: {result['description']}")
            print("-" * 80)
        save_option = input("Save results? (csv/json/no): ").strip().lower()
        if save_option == 'csv':
            filename = input("CSV filename (default google_search_results.csv): ") or "google_search_results.csv"
            scraper.save_to_csv(filename)
        elif save_option == 'json':
            filename = input("JSON filename (default google_search_results.json): ") or "google_search_results.json"
            scraper.save_to_json(filename)
    except KeyboardInterrupt:
        print("\n[INFO] Scraping interrupted.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
