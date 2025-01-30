import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class Selenium_Scraper:
    def __init__(self, num_pages=5):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        
        self.num_pages = num_pages
        self.base_url = "https://www.google.com/search"
        self.all_results = []

    def perform_multi_page_search(self, query):
    
        try:
            self.all_results = []
            for page in range(self.num_pages):

                start = page * 10

                search_url = (
                    f"{self.base_url}?"
                    f"q={query.replace(' ', '+')}"
                    f"&start={start}"
                )
                
               
                self.driver.get(search_url)
                
                self._wait_for_results()
                
                page_results = self._extract_page_results()
                
                self.all_results.extend(page_results)
                
                time.sleep(2)
            
            return self.all_results
        
        except Exception as e:
            print(f"Multi-page search error: {e}")
            return []

    def _wait_for_results(self, timeout=10):
 
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
            )
        except TimeoutException:
            print("Timeout: Search results did not load in time.")

    def _extract_page_results(self):

        page_results = []
        
        try:
 
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for result in search_results:
                try:
                
                    title = result.find_element(By.TAG_NAME, "h3").text
                    
                    link_element = result.find_element(By.TAG_NAME, "a")
                    link = link_element.get_attribute("href")
                    
                    try:
                        snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    except NoSuchElementException:
                        snippet = "No snippet available"
                    
                    result_dict = {
                        "Title": title,
                        "Link": link,
                        "Snippet": snippet
                    }
                    
                    page_results.append(result_dict)
                
                except Exception as inner_e:
                    print(f"Error extracting individual result: {inner_e}")
        
        except Exception as e:
            print(f"Page results extraction error: {e}")
        
        return page_results

    def save_to_csv(self, results=None, filename=None):

        if results is None:
            results = self.all_results
        
        if filename is None:
            filename = f"google_search_results_{int(time.time())}.csv"
        
        try:

            os.makedirs("results", exist_ok=True)
            
            full_path = os.path.join("results", filename)
            
            df = pd.DataFrame(results)
            df.to_csv(full_path, index=False, encoding='utf-8')
            
            print(f"Results saved to {full_path}")
            print(f"Total results saved: {len(results)}")
        
        except Exception as e:
            print(f"CSV saving error: {e}")

    def close(self):

        self.driver.quit()

def main():

    num_pages = int(input("Enter the number of pages to scrape: "))
    scraper = Selenium_Scraper(num_pages=num_pages)
    
    try:
        time.sleep(2)
        query = input("Enter search query: ").strip()
        
        results = scraper.perform_multi_page_search(query)
        
        if results:
            filename = f"{query.replace(' ', '_')}_results.csv"
            scraper.save_to_csv(filename=filename)
        else:
            print("No results found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:

        scraper.close()

if __name__ == "__main__":
    main()