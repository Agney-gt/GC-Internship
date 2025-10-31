# google_scraper_unique.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

class GoogleResultFetcher:
    def __init__(self, search_term: str, scroll_times: int = 2, delay: int = 2):
        """Initialize the Chrome WebDriver and open the Google search results page."""
        self.search_term = search_term
        self.scroll_times = scroll_times
        self.delay = delay
        self.results_data = []

        print(f"[SETUP] Launching Chrome browser...")
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
        self.browser.get(search_url)
        time.sleep(self.delay)
        print(f"[INFO] Searching Google for: '{search_term}'")

    def auto_scroll(self):
        """Automatically scroll the page down to load more search results."""
        print("[ACTION] Scrolling the page to fetch more results...")
        body = self.browser.find_element(By.TAG_NAME, "body")
        for _ in range(self.scroll_times):
            body.send_keys(Keys.END)
            time.sleep(self.delay)

    def collect_data(self):
        """Collects the titles and URLs from Google search results."""
        print("[SCRAPING] Gathering result titles and URLs...")
        items = self.browser.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")

        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, "h3").text
                url = item.get_attribute("href")
                self.results_data.append({"Title": title, "URL": url})
            except Exception as e:
                print(f"[WARNING] Skipped one result due to: {e}")

        print(f"[DONE] Collected {len(self.results_data)} search results.")

    def export_csv(self, filename="google_search_output.csv"):
        """Saves the collected results into a CSV file."""
        df = pd.DataFrame(self.results_data)
        df.to_csv(filename, index=False)
        print(f"[SAVED] Data exported successfully to '{filename}'")

    def shutdown(self):
        """Close the browser window."""
        self.browser.quit()
        print("[EXIT] Browser closed successfully.")


# --- Run the script ---
if __name__ == "__main__":
    print("✨ Starting Google Search Fetcher ✨")
    fetcher = GoogleResultFetcher(search_term="Top 10 programming languages 2025")
    fetcher.auto_scroll()
    fetcher.collect_data()
    fetcher.export_csv("Keerthana_google_results.csv")
    fetcher.shutdown()
    print("✅ All done!")
