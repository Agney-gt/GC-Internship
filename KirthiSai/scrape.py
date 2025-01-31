import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class GoogleScraper:
    def __init__(self, query, num_scrolls=3):
        self.query = query
        self.num_scrolls = num_scrolls
        self.driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH
        self.results = []

    def scrape(self):
        # Navigate to Google search
        self.driver.get(f"https://www.google.com/search?q={self.query}")
        print("[INFO]: Opened Google search page.")

        # Scroll the page to load more results
        for _ in range(self.num_scrolls):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(5)

        # Extract search results
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")
        for element in elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, "h3").text
                url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = element.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                self.results.append({"Title": title, "URL": url, "Description": description})
            except Exception as e:
                print(f"[WARNING]: Skipping element due to error: {e}")

        print("[INFO]: Scraping complete.")
        self.driver.quit()

    def save_to_csv(self, file_name="google_results.csv"):
        df = pd.DataFrame(self.results)
        df.to_csv(file_name, index=False)
        print(f"[INFO]: Results saved to {file_name}")


if __name__ == "__main__":
    search_query = input("Enter search query: ")
    scraper = GoogleScraper(query=search_query)
    scraper.scrape()
    scraper.save_to_csv("search_results.csv")
