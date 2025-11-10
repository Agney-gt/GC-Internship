from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_google_search(query):
    # Setup Chrome driver
    driver = webdriver.Chrome()
    
    try:
        # Open Google
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Find search box and enter query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Scrape search results
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        
        print(f"Search results for: {query}\n")
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    query = input("Enter search query: ")
    scrape_google_search(query)