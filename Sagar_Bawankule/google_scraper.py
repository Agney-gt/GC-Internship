"""
Google Search Results Scraper using Selenium
This script scrapes Google search results for a given query.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import csv
import json


class GoogleScraper:
    """A class to scrape Google search results using Selenium."""
    
    def __init__(self, headless=False):
        """
        Initialize the scraper with Chrome options.
        
        Args:
            headless (bool): Run browser in headless mode if True
        """
        self.options = Options()
        
        if headless:
            self.options.add_argument('--headless')
        
        # Add arguments to avoid detection
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--start-maximized')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent to look more like a real browser
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = None
        self.results = []
    
    def start_driver(self):
        """Start the Chrome WebDriver."""
        try:
            self.driver = webdriver.Chrome(options=self.options)
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("Chrome WebDriver started successfully.")
        except Exception as e:
            print(f"Error starting WebDriver: {e}")
            raise
    
    def search_google(self, query, num_results=10):
        """
        Search Google for the given query and scrape results.
        
        Args:
            query (str): The search query
            num_results (int): Number of results to scrape (default: 10)
        
        Returns:
            list: List of dictionaries containing search results
        """
        if not self.driver:
            self.start_driver()
        
        try:
            # Navigate to Google
            print(f"Searching for: {query}")
            self.driver.get("https://www.google.com")
            
            # Wait for search box to be present
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Enter search query and submit
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Scrape the results
            self.results = self._extract_results(num_results)
            
            print(f"Successfully scraped {len(self.results)} results.")
            return self.results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def _extract_results(self, num_results):
        """
        Extract search results from the current page.
        
        Args:
            num_results (int): Maximum number of results to extract
        
        Returns:
            list: List of dictionaries with result data
        """
        results = []
        
        try:
            # Find all search result divs
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for index, result in enumerate(search_results[:num_results], 1):
                try:
                    # Extract title
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text if title_element else "N/A"
                    
                    # Extract URL
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    url = link_element.get_attribute("href") if link_element else "N/A"
                    
                    # Extract description/snippet
                    try:
                        description_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                        description = description_element.text
                    except:
                        description = "N/A"
                    
                    # Store the result
                    result_data = {
                        'rank': index,
                        'title': title,
                        'url': url,
                        'description': description
                    }
                    
                    results.append(result_data)
                    print(f"Result {index}: {title}")
                    
                except Exception as e:
                    print(f"Error extracting result {index}: {e}")
                    continue
            
        except Exception as e:
            print(f"Error finding search results: {e}")
        
        return results
    
    def save_to_csv(self, filename="google_search_results.csv"):
        """
        Save the scraped results to a CSV file.
        
        Args:
            filename (str): Name of the CSV file
        """
        if not self.results:
            print("No results to save.")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['rank', 'title', 'url', 'description'])
                writer.writeheader()
                writer.writerows(self.results)
            
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def save_to_json(self, filename="google_search_results.json"):
        """
        Save the scraped results to a JSON file.
        
        Args:
            filename (str): Name of the JSON file
        """
        if not self.results:
            print("No results to save.")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.results, file, indent=4, ensure_ascii=False)
            
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("WebDriver closed.")


def main():
    """Main function to demonstrate the scraper."""
    
    # Create scraper instance
    scraper = GoogleScraper(headless=False)  # Set to True for headless mode
    
    try:
        # Get search query from user
        query = input("Enter your search query: ")
        num_results = int(input("How many results do you want to scrape? (default 10): ") or "10")
        
        # Perform search
        results = scraper.search_google(query, num_results)
        
        # Display results
        print("\n" + "="*80)
        print("SEARCH RESULTS")
        print("="*80 + "\n")
        
        for result in results:
            print(f"Rank: {result['rank']}")
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Description: {result['description']}")
            print("-" * 80)
        
        # Ask user if they want to save results
        save_option = input("\nDo you want to save the results? (csv/json/no): ").lower()
        
        if save_option == 'csv':
            scraper.save_to_csv()
        elif save_option == 'json':
            scraper.save_to_json()
        else:
            print("Results not saved.")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        scraper.close()


if __name__ == "__main__":
    main()
