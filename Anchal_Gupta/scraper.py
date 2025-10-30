from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
import csv
import pandas as pd



class GoogleSearchScraper:
    def __init__(self, query: str, n_scrolls: int = 2):
        """Initialize Chrome driver and search query."""
        self.query = query
        self.n_scrolls = n_scrolls
        self.titles = []
        self.links = []

        print("[INFO] Initializing browser...")
        self.driver = webdriver.Chrome()
        self.driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(2)
        print(f"[INFO] Searching for '{query}'")

    def scroll_page(self):
        """Scroll down the page to load more results."""
        for _ in range(self.n_scrolls):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)

    def extract_results(self):
        """Extract result titles and URLs."""
        print("[INFO] Extracting search results...")
        results = self.driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")

        for result in results:
            title_element = result.find_element(By.TAG_NAME, "h3")
            self.titles.append(title_element.text)
            self.links.append(result.get_attribute("href"))

        print(f"[INFO] Extracted {len(self.titles)} results.")

    def save_to_csv(self, file_path="search_results.csv"):
        """Save the data to a CSV file."""
        df = pd.DataFrame({"Title": self.titles, "URL": self.links})
        df.to_csv(file_path, index=False)
        print(f"[INFO] Results saved to {file_path}")

    def close(self):
        """Close the browser."""
        self.driver.quit()
        print("[INFO] Browser closed.")


if __name__ == "__main__":
    scraper = GoogleSearchScraper(query="Top 10 programming languages 2025")
    scraper.scroll_page()
    scraper.extract_results()
    scraper.save_to_csv("anchal_gupta_results.csv")
    scraper.close()
