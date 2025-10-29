from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import json
import os

class GoogleScraper:
    def __init__(self, query, limit=10, headless=True):
        self.query = query
        self.limit = limit
        self.results = []
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def search_google(self):
        print(f"🔍 Searching Google for: {self.query}")
        self.driver.get("https://www.google.com")
        time.sleep(1)

        # Handle cookie popup (optional)
        try:
            self.driver.find_element(By.XPATH, "//button[contains(.,'Accept')]").click()
        except:
            pass

        # Enter query
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(self.query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

    def fetch_results(self):
        print(f"📄 Fetching top {self.limit} results...")

        # Scroll to load more results (if needed)
        for _ in range(2):
            self.driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(1)

        items = self.driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")  # each search card
        for i, item in enumerate(items[:self.limit], start=1):
            try:
                title = item.find_element(By.CSS_SELECTOR, "h3").text
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                snippet = item.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                self.results.append({
                    "rank": i,
                    "title": title,
                    "url": link,
                    "snippet": snippet
                })
            except Exception as e:
                print(f"⚠️ Skipping a result due to error: {e}")
        print("✅ Data fetched successfully!")

    def save_results(self):
        os.makedirs("output", exist_ok=True)
        filename = f"output/google_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "query": self.query,
                "timestamp": str(datetime.now()),
                "results": self.results
            }, f, indent=4, ensure_ascii=False)
        print(f"💾 Results saved to: {filename}")
        return filename

    def close(self):
        self.driver.quit()

    def run(self):
        try:
            self.search_google()
            self.fetch_results()
            return self.save_results()
        finally:
            self.close()


if __name__ == "__main__":
    scraper = GoogleScraper(query="AI internship opportunities in India 2025", limit=10, headless=False)
    file = scraper.run()
    print(f"🎉 Data collection complete! Check file: {file}")
