from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def setup_driver():
    """Setup Chrome WebDriver with advanced anti-detection options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_google_results(search_query, num_results=10):
    """Scrape Google search results with advanced handling"""
    driver = setup_driver()
    
    try:
        # Navigate to Google
        driver.get('https://www.google.com')
        time.sleep(2)
        
        # Find and fill search input
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g, div.yuRUbf'))
        )
        
        # Collect results
        results = []
        
        # Multiple potential selectors for maximum compatibility
        title_selectors = [
            'h3', 
            'div.yuRUbf h3', 
            'div.r h3'
        ]
        
        snippet_selectors = [
            'div.VwiC3b', 
            'div.IsZvec', 
            'div.s', 
            'div.summary'
        ]
        
        for selector in title_selectors:
            try:
                search_results = driver.find_elements(By.CSS_SELECTOR, f'{selector} + div.g, div.g')
                
                for result in search_results[:num_results]:
                    try:
                        # Extract title
                        title_elem = result.find_element(By.CSS_SELECTOR, selector)
                        title = title_elem.text
                        
                        # Extract link
                        link_elem = result.find_element(By.CSS_SELECTOR, 'a')
                        link = link_elem.get_attribute('href')
                        
                        # Extract snippet (try multiple selectors)
                        snippet = "No snippet available"
                        for snippet_selector in snippet_selectors:
                            try:
                                snippet_elem = result.find_element(By.CSS_SELECTOR, snippet_selector)
                                snippet = snippet_elem.text
                                break
                            except:
                                continue
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                    except Exception as e:
                        print(f"Individual result extraction error: {e}")
                
                # If results found, break the selector loop
                if results:
                    break
            except Exception as e:
                print(f"Result search error with selector {selector}: {e}")
        
        return results
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []
    
    finally:
        driver.quit()

def main():
    search_term = "Python programming"
    results = scrape_google_results(search_term)
    
    if results:
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}\n")
        
        # Save to CSV
        with open('google_search_results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'snippet'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Saved {len(results)} results to google_search_results.csv")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()