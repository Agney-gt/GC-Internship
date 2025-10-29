import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class CustomGoogleScraper:
    def __init__(self, query: str, scrolls: int = 3, headless: bool = True):
        
        self.query = query
        self.scrolls = scrolls
        self.headless = headless
        self.results = []

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def load_results(self):
     
        self.driver.get(f"https://www.google.com/search?q={self.query}")
        print("[INFO]: Google search page loaded.")

        for i in range(self.scrolls):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)  # Allow results to load
            print(f"[INFO]: Completed scroll {i + 1}/{self.scrolls}.")

    def scrape_results(self):
       
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")
        print(f"[INFO]: Found {len(elements)} results to scrape.")

        for element in elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, "h3").text
                url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = element.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                self.results.append({"Title": title, "URL": url, "Description": description})
            except Exception as e:
                print(f"[WARNING]: Skipping an element due to error: {e}")

    def save_results(self, file_name: str = "google_results.csv"):
        
        if not self.results:
            print("[INFO]: No results to save.")
            return

        df = pd.DataFrame(self.results)
        df.to_csv(file_name, index=False)
        print(f"[INFO]: Results successfully saved to {file_name}.")

    def close(self):

        self.driver.quit()

    def run(self):

        try:
            self.load_results()
            self.scrape_results()
            self.save_results()
        except Exception as e:
            print(f"[ERROR]: An unexpected error occurred: {e}")
        finally:
            self.close()


if __name__ == "__main__":
    print("[INFO]: Welcome to the Custom Google Scraper!")
    user_query = input("Enter your search query: ")
    user_scrolls = int(input("How many scrolls do you want to perform? (Recommended: 3): "))

    print("\n[INFO]: Starting the scraper. Please ensure responsible usage of this tool.\n")

    scraper = CustomGoogleScraper(query=user_query, scrolls=user_scrolls, headless=False)
    scraper.run()

    print("\n[INFO]: Task completed. Results saved successfully.")