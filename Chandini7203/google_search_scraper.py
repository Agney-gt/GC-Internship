from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys

def setup_driver(headless=True):
    """
    Set up Chrome WebDriver with options.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_google_search(query, num_results=10):
    """
    Scrape Google search results for a given query.
    
    Args:
        query (str): Search query
        num_results (int): Number of results to scrape (default: 10)
    
    Returns:
        list: List of dictionaries containing title, link, and snippet
    """
    driver = setup_driver(headless=True)
    results = []
    
    try:
        # Navigate to Google
        driver.get('https://www.google.com')
        time.sleep(2)
        
        # Handle cookie consent if present
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree')]"))
            )
            consent_button.click()
            time.sleep(1)
        except TimeoutException:
            pass  # No consent button found, continue
        
        # Find search box and enter query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )
        time.sleep(2)
        
        # Find all result blocks
        result_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.g')
        
        print(f"\nFound {len(result_blocks)} search results for query: '{query}'\n")
        print("=" * 80)
        
        count = 0
        for block in result_blocks:
            if count >= num_results:
                break
            
            try:
                # Extract title
                title_elem = block.find_element(By.CSS_SELECTOR, 'h3')
                title = title_elem.text.strip()
                
                # Extract link
                link_elem = block.find_element(By.CSS_SELECTOR, 'a')
                link = link_elem.get_attribute('href')
                
                # Extract snippet
                snippet = ""
                try:
                    snippet_elem = block.find_element(By.CSS_SELECTOR, 'div.VwiC3b, div.IsZvec, span.aCOpRe')
                    snippet = snippet_elem.text.strip()
                except NoSuchElementException:
                    snippet = "No snippet available"
                
                # Skip if no title or link
                if not title or not link:
                    continue
                
                result = {
                    'title': title,
                    'link': link,
                    'snippet': snippet
                }
                results.append(result)
                
                # Print result
                print(f"Result {count + 1}:")
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Snippet: {snippet}")
                print("-" * 80)
                
                count += 1
                
            except NoSuchElementException:
                continue
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()
    
    return results

if __name__ == '__main__':
    # Default query if no arguments provided
    if len(sys.argv) > 1:
        search_query = ' '.join(sys.argv[1:])
    else:
        search_query = 'Python programming'
    
    # Number of results to fetch
    num_results = 10
    
    print(f"\nStarting Google search scraper...")
    print(f"Query: {search_query}")
    print(f"Number of results: {num_results}\n")
    
    # Scrape Google search results
    search_results = scrape_google_search(search_query, num_results)
    
    print(f"\n\nTotal results scraped: {len(search_results)}")
    print("\nScraping completed successfully!")
