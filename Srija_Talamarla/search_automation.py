from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from save_results import save_results, sanitize_query

def setup_driver():
    chrome_options = Options()
    # Disable automation flags to avoid detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    # Mask selenium's presence
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def google_search(query, num_results=10):
    driver = setup_driver()
    results = []
    seen_links = set()  # Track duplicate links
    page = 1
    
    try:
        # Navigate to Google and search
        driver.get('https://www.google.com')
        time.sleep(1)
        
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        while len(results) < num_results:  # Limit to 3 pages
            time.sleep(3)  # Wait for page load
            
            # Find search results
            results_selector = "div.g"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, results_selector))
            )
            
            search_results = driver.find_elements(By.CSS_SELECTOR, results_selector)
            
            for result in search_results:
                if len(results) >= num_results:
                    break
                    
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text
                    
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    link = link_element.get_attribute("href")
                    
                    # Skip duplicates
                    if link in seen_links:
                        continue
                        
                    try:
                        description = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                    except:
                        description = "No description available"
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'link': link,
                            'description': description
                        })
                        seen_links.add(link)
                        
                except Exception as e:
                    print(f"Error extracting a result: {str(e)}")
                    continue
            
            # Go to next page if we need more results
            if len(results) < num_results:
                try:
                    next_button = driver.find_element(By.ID, "pnnext")
                    next_button.click()
                    page += 1
                except:
                    print("No more pages available")
                    break
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()
        
    return results[:num_results]


def main():
    search_query = input("Enter your search query: ")
    num_results = int(input("How many results do you want? "))
    
    print(f"\nSearching for: {search_query}")
    results = google_search(search_query, num_results)
    
    print(f"\nFound {len(results)} results:")
    print("-" * 50)
    
    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. {result['title']}")
        print(f"   Link: {result['link']}")
        print(f"   Description: {result['description'][:150]}...")  # Truncate long descriptions

    if results:
        save_prompt = input("\nDo you want to save the results? (yes/no): ").strip().lower()
        if save_prompt == 'yes':
            sanitized_query = sanitize_query(search_query)
            save_results(results, sanitized_query)
        else:
            print("Results were not saved.")

if __name__ == "__main__":
    main()