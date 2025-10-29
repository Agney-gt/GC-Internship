from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time

class GoogleScraper:
    def __init__(self, headless=False, timeout=10):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            
    def start_driver(self):
        """Initialize the Chrome driver"""
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        
    def search(self, query, max_results=10):
        """Perform Google search and extract results"""
        if not self.driver:
            self.start_driver()
            
        # Check if driver and wait were properly initialized
        if not self.driver or not self.wait:
            print("Failed to initialize web driver")
            return []
            
        try:
            print(f"Searching for: {query}")
            # Navigate to Google
            self.driver.get("https://www.google.com")
            
            # Find and fill search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            self.wait.until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Extract results
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            output = []
            
            for idx, result in enumerate(results[:max_results], start=1):
                try:
                    # Extract title
                    title_elem = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_elem.text
                except NoSuchElementException:
                    title = "No title found"
                
                try:
                    # Extract link
                    link_elem = result.find_element(By.TAG_NAME, "a")
                    link = link_elem.get_attribute("href")
                except NoSuchElementException:
                    link = "No link found"
                    
                try:
                    # Extract snippet (description)
                    snippet_elem = result.find_element(By.CSS_SELECTOR, "span")
                    snippet = snippet_elem.text
                except NoSuchElementException:
                    snippet = "No description available"
                    
                try:
                    # Extract additional info if available
                    additional_info = ""
                    try:
                        additional_elem = result.find_element(By.CSS_SELECTOR, ".MUxGbd")
                        additional_info = additional_elem.text
                    except NoSuchElementException:
                        pass
                except:
                    additional_info = ""

                output.append({
                    "rank": idx,
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "additional_info": additional_info
                })

            return output
            
        except TimeoutException:
            print("Page load timeout occurred")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
            
    def save_to_json(self, results, filename="search_results.json"):
        """Save results to JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")
        
    def print_results(self, results):
        """Print results in a formatted way"""
        if not results:
            print("No results found.")
            return
            
        print(f"\nFound {len(results)} results:\n")
        for result in results:
            print(f"{result['rank']}. {result['title']}")
            print(f"   URL: {result['link']}")
            if result['snippet']:
                print(f"   Snippet: {result['snippet'][:150]}...")
            if result['additional_info']:
                print(f"   Additional: {result['additional_info']}")
            print("-" * 80)

def main():
    # Example usage of the GoogleScraper class
    query = "Machine learning tutorials"
    
    with GoogleScraper(headless=False, timeout=15) as scraper:
        results = scraper.search(query, max_results=8)
        scraper.print_results(results)
        scraper.save_to_json(results, f"{query.replace(' ', '_')}_results.json")

if __name__ == "__main__":
    main()