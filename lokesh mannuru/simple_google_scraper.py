"""
Simple Google Scraper using Selenium
This script demonstrates how to scrape Google search results using Selenium.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

def scrape_google_results(query, num_results=5):
    """
    Scrape Google search results for a given query
    
    Args:
        query (str): The search query
        num_results (int): Number of results to fetch (default: 5)
    
    Returns:
        list: List of dictionaries containing search result data
    """
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = None
    try:
        # Initialize the Chrome driver
        # Note: This requires ChromeDriver to be installed and in PATH
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Google
        driver.get("https://www.google.com")
        
        # Find the search box and enter the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for results to load
        time.sleep(2)
        
        # Collect results
        results = []
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        
        for i, result in enumerate(search_results[:num_results]):
            try:
                # Extract title
                title_element = result.find_element(By.CSS_SELECTOR, "h3")
                title = title_element.text
                
                # Extract URL
                url_element = result.find_element(By.CSS_SELECTOR, "a")
                url = url_element.get_attribute("href")
                
                # Extract snippet (description)
                try:
                    snippet_element = result.find_element(By.CSS_SELECTOR, "span")
                    snippet = snippet_element.text
                except:
                    snippet = "No snippet available"
                
                results.append({
                    "rank": i + 1,
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })
            except Exception as e:
                # Skip this result if there's an error extracting data
                continue
        
        return results
    
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        print("Make sure ChromeDriver is installed and in your PATH")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
    finally:
        # Close the driver if it was opened
        if driver:
            driver.quit()

def main():
    """Main function to demonstrate the scraper"""
    query = "Python programming"
    
    print(f"Searching for: {query}")
    print("=" * 60)
    
    try:
        results = scrape_google_results(query)
        
        if results:
            print(f"Found {len(results)} results:\n")
            for result in results:
                print(f"Rank: {result['rank']}")
                print(f"Title: {result['title']}")
                print(f"URL: {result['url']}")
                print(f"Snippet: {result['snippet']}")
                print("-" * 60)
        else:
            print("No results found or an error occurred.")
            print("\nNote: This script requires:")
            print("1. Google Chrome browser installed")
            print("2. ChromeDriver installed and in your system PATH")
            print("3. Selenium package (pip install selenium)")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()