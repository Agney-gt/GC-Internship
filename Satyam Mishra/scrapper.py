import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time


class GoogleScraper:
    def __init__(self, query, num_scrolls=3, headless=False):
        self.query = query
        self.num_scrolls = num_scrolls
        self.results = []
        self.driver = self._initialize_driver(headless)

    def _initialize_driver(self, headless):
        """Initialize the Chrome WebDriver."""
        options = Options()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        service = Service()
        return webdriver.Chrome(service=service, options=options)

    def scrape(self):
        """Perform the scraping process."""
        try:
            self._navigate_to_search()
            self._scroll_and_collect_results()
        except Exception as e:
            print(f"[ERROR]: An unexpected error occurred: {e}")
        finally:
            self.driver.quit()
            print("[INFO]: WebDriver closed.")

    def _navigate_to_search(self):
        """Navigate to the Google search page."""
        self.driver.get(f"https://www.google.com/search?q={self.query}")
        print("[INFO]: Opened Google search page.")

    def _scroll_and_collect_results(self):
        """Scroll the page and collect search results."""
        for scroll in range(self.num_scrolls):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            print(f"[INFO]: Scrolled {scroll + 1}/{self.num_scrolls} times.")
            time.sleep(2)

        self._extract_results()

    def _extract_results(self):
        """Extract search results from the page."""
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")
        for idx, element in enumerate(elements):
            try:
                title = element.find_element(By.CSS_SELECTOR, "h3").text
                url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = element.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                self.results.append({"Title": title, "URL": url, "Description": description})
                print(f"[INFO]: Extracted result {idx + 1}.")
            except NoSuchElementException as e:
                print(f"[WARNING]: Skipping result due to missing element: {e}")

    def save_to_csv(self, file_name="google_results.csv"):
        """Save the results to a CSV file."""
        if not self.results:
            print("[INFO]: No results to save.")
            return
        df = pd.DataFrame(self.results)
        df.to_csv(file_name, index=False)
        print(f"[INFO]: Results saved to {file_name}.")


if __name__ == "__main__":
    query = input("Enter search query: ")
    num_scrolls = int(input("Enter number of scrolls: "))
    headless = input("Run in headless mode? (yes/no): ").strip().lower() == "yes"

    scraper = GoogleScraper(query=query, num_scrolls=num_scrolls, headless=headless)
    scraper.scrape()
    scraper.save_to_csv("search_results.csv")
