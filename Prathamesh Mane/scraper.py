import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GoogleSearchScraper:
    def __init__(self, search_term: str, num_scrolls: int = 3, is_headless: bool = True):
        self.search_term = search_term
        self.num_scrolls = num_scrolls
        self.is_headless = is_headless
        self.search_results = []

        # Configure Chrome options
        options = Options()
        if is_headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Initialize WebDriver
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def open_search_page(self):
        """Navigate to Google search results for the given query."""
        self.browser.get(f"https://www.google.com/search?q={self.search_term}")
        print("[INFO] Google search page is loaded and ready.")

        # Perform scrolling to load more results
        for i in range(self.num_scrolls):
            self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)  # Allow time for additional results to load
            print(f"[INFO] Scrolled down ({i + 1}/{self.num_scrolls}).")

    def extract_results(self):
        """Scrape the search results."""
        elements = self.browser.find_elements(By.CSS_SELECTOR, "div.MjjYud")
        print(f"[INFO] Located {len(elements)} search result entries.")

        for element in elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, "h3").text
                url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = element.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                self.search_results.append({"Title": title, "URL": url, "Description": description})
            except Exception as e:
                print(f"[WARNING] Unable to scrape an entry. Skipping. Error: {e}")

    def show_results(self):
        """Display the search results in a clean format."""
        if not self.search_results:
            print("[INFO] No results found to display.")
            return

        print("\n[INFO] Here are the search results:\n")
        for i, result in enumerate(self.search_results, start=1):
            print(f"Result {i}:")
            print(f"- Title: {result['Title']}")
            print(f"- URL: {result['URL']}")
            print(f"- Description: {result['Description']}\n")

    def close_browser(self):
        """Close the browser session."""
        self.browser.quit()

    def start(self):
        """Run the full scraping process."""
        try:
            print("\n[INFO] Starting Google Search Scraper...")
            self.open_search_page()
            self.extract_results()
            self.show_results()
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")
        finally:
            self.close_browser()
            print("\n[INFO] Scraper has completed its task and closed the browser.")


if __name__ == "__main__":
    print("[INFO] Welcome to the Google Search Scraper!")
    query = input("Enter the search query: ")
    scroll_count = int(input("Enter the number of scrolls (default is 3): "))

    print("\n[INFO] Initializing scraper with your query. Please wait...\n")

    scraper = GoogleSearchScraper(search_term=query, num_scrolls=scroll_count, is_headless=False)
    scraper.start()
