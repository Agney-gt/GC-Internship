from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def google_search_scraper(search_query, num_results=5):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # Uncomment the line below if you want to run Chrome in headless mode
    # chrome_options.add_argument("--headless")
    
    # Initialize the driver with options
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        time.sleep(2)  # Wait for page to load completely
        
        # Find and click accept cookies button if it exists
        try:
            accept_button = driver.find_element(By.ID, "L2AGLb")
            accept_button.click()
            time.sleep(1)
        except:
            pass  # If no cookie banner, continue
        
        # Find the search box and enter query
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        time.sleep(3)  # Give more time for results to load
        
        # Get search results using different selectors
        results = []
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        
        for i, result in enumerate(search_results):
            if i >= num_results:
                break
                
            try:
                # Try different possible selectors for title and link
                try:
                    title = result.find_element(By.CSS_SELECTOR, "h3").text
                except:
                    continue
                    
                try:
                    link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                except:
                    link = "Link not found"
                    
                try:
                    snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                except:
                    snippet = "Snippet not found"
                
                if title and title.strip():  # Only add if title is not empty
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
                    
            except Exception as e:
                print(f"Error extracting result {i}: {e}")
                continue
                
        return results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Example usage
    search_query = "Python programming"
    results = google_search_scraper(search_query)
    
    if results:
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
    else:
        print("No results found or an error occurred")