# GC_Internship onboarding Task: Google Search Scraper
# This script uses Selenium to scrape Google search results based on a user-defined query.
# Author: Manikant Kumar

# Important highlights:
# user based input for search query and number of results.
# each search result includes heading, snippet, and link.
# each time the script runs, it saves results to a CSV file named according to the search query.
# There are 5 search results I have included with this python file.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


class GoogleSearchScraper:
    def __init__(self, query=str, pages_count=1, result_limit=10):
        self.driver = webdriver.Chrome()
        self.query = query
        self.pages_count = pages_count
        self.result_limit = result_limit
        self.links, self.headings, self.snippets = [], [], []

    def search(self):
        self.driver.get(f"https://www.google.com/search?q={self.query}")
        print("[INFO]: Successfully connected to Google.")
        self.collect_results()

        for _ in range(self.pages_count):
            try:
                next_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "pnnext"))
                )
                next_button.click()
                time.sleep(10)
                self.collect_results()
            except Exception:
                print("[WARN]: No more pages available.")
                break

    def collect_results(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tF2Cxc"))
            )

            results = self.driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
            for item in results:
                if len(self.headings) >= self.result_limit:
                    break

                try:
                    title = item.find_element(By.CSS_SELECTOR, "h3").text
                    snippet = item.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    self.headings.append(title)
                    self.snippets.append(snippet)
                    self.links.append(link)
                except Exception:
                    continue

            print(f"[INFO]: Collected {len(self.headings)} results so far.")
        except Exception as e:
            print(f"[ERROR]: Could not collect results - {e}")

    def save_results(self):
        data = {
            "Heading": self.headings,
            "Snippet": self.snippets,
            "Link": self.links
        }
        return pd.DataFrame(data)

    def save_to_csv(self, file_name: str):
        df = self.save_results()
        df.to_csv(file_name, index=False)
        print(f"[INFO]: Data saved to {file_name}")

    def close(self):
        self.driver.quit()
        print("[INFO]: Browser closed.")


if __name__ == "__main__":
    user_query = input("Enter Search Query: ").strip()
    result_count = int(input("Enter number of required results: "))
    scraper = GoogleSearchScraper(query=user_query, pages_count=int(result_count//10), result_limit=result_count)
    scraper.search()
    scraper.save_to_csv(f"google_search_{user_query}_scrape_results.csv")
    scraper.close()
