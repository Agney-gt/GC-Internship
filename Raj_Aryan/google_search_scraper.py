from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class Scraper:
    def __init__(self,query,headless):
        self.query = query
        self.result = []
        self.headless = headless
        self.setup_driver(self.headless)

    def setup_driver(self,headless):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")


        self.driver = webdriver.Chrome(options=options)


    def main_scraper(self):
        self.driver.get(f"https://google.com/search?q={self.query}")
        try:
            print(f"STARTING THE DRIVER")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"div.tF2Cxc"))
            )
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
            # print(f'PRINTING ELEMENTS: {elements}')
            for element in elements:
                try:
                    title = element.find_element(By.CSS_SELECTOR, "h3").text
                    link = element.find_element(By.TAG_NAME, "a").get_attribute('href')
                    description = element.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    print(f"PRINTING EVERYTHING "
                          f"title:{title} "
                          f"link:{link} "
                          f"Description: {description}"
                          )
                    self.result.append({"title": title, "link": link, "description": {description}})
                except Exception as e:
                    print(f'Error Skipping a result due to error: {e}')
        except Exception as e:
            print(f'Failed to load results {e}')

    def close(self):
        self.driver.close()

    def run(self):
        try:
            self.main_scraper()
        except Exception as e:
            print(f'Error Occured: {e}')
        finally:
            self.close()
if __name__ == "__main__":
    print("SCRAPER STARTED:")

    query = input("Please enter the search query: ")

    scraper = Scraper(query=query,headless=False)
    scraper.run()

    print(f"All data Found")
