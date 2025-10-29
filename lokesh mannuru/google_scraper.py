import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_google_results(query, num_results=10):
    """
    Scrape Google search results for a given query
    
    Args:
        query (str): The search query
        num_results (int): Number of results to fetch (default: 10)
    
    Returns:
        list: List of dictionaries containing search result data
    """
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        
        # Wait for the search box to load
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Enter the search query
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
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
                snippet_element = result.find_element(By.CSS_SELECTOR, "span")
                snippet = snippet_element.text
                
                results.append({
                    "rank": i + 1,
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })
            except Exception as e:
                print(f"Error extracting result {i+1}: {e}")
                continue
        
        return results
    
    finally:
        # Close the driver
        driver.quit()

def main():
    """Main function to demonstrate the scraper"""
    query = "Python programming"
    
    print(f"\nSearching for: {query}")
    print("-" * 50)
    
    try:
        results = scrape_google_results(query)
        
        if results:
            for result in results:
                print(f"\nRank: {result['rank']}")
                print(f"Title: {result['title']}")
                print(f"URL: {result['url']}")
                print(f"Snippet: {result['snippet']}")
                print("-" * 50)
        else:
            print("No results found.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# For demonstration purposes, we'll run the main function
# In a real environment, you would uncomment the lines below
# if __name__ == "__main__":
#     main()

# Running the function directly for this demo
main()