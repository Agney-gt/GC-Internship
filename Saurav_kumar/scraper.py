from selenium import webdriver
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36'
] #to avoid getting blocked by the google.

class Scraper:
    driver = None
    def __init__(self,chrome_path):
        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        chrome_options.add_argument("--headless")#to run the scraping in the background.
        chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def scrapeData(self,searchString):
        self.driver.get(f"https://www.google.com/search?q={searchString}")
        print("scraping data....");
        result = self.driver.find_elements(By.TAG_NAME, "h3")
        headings = []
        for heading in result:
            headings.append(heading.text)

        return headings
if __name__ == "__main__":
    scraper = Scraper(r"C:\Program Files\Google\Chrome\Application\chrome.exe")#chrome path
    links = scraper.scrapeData("hellow")
    if(len(links) > 0):
        print(links)
    else:
        print("No data found! Google might have blocked the request.")

        
        
