import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_google_results(query, num_results=5, headless=False):
    """
    Scrapes Google search results for a given query using Selenium.
    
    Args:
        query (str): The search term to look for.
        num_results (int): The number of results to retrieve.
        headless (bool): Whether to run browser in headless mode.
    
    Returns:
        list: List of dictionaries containing title, link, and snippet.
    """
    print(f"Starting scraper for query: '{query}'...")
    
    results_data = []
    driver = None
    
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        
        # Run in headless mode (no browser window)
        if headless:
            options.add_argument("--headless")
        
        # Additional options to avoid detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Exclude automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Go to Google
        print("Navigating to Google...")
        driver.get("https://www.google.com")
        
        # Wait for search box to be present
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        
        # Type in the query and press Enter
        print(f"Searching for: {query}")
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
        
        # Wait for results to load (wait for at least one result)
        print("Waiting for results to load...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))
        
        # Give a bit more time for all results to render
        time.sleep(2)
        
        # Find all result elements
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        
        if not results:
            print("No results found. Google might have blocked the request or changed its layout.")
            return results_data
        
        print(f"Found {len(results)} results. Processing top {num_results}...")
        
        # Loop through the top results and extract data
        for i, result in enumerate(results[:num_results]):
            try:
                # Extract title
                title_element = result.find_element(By.TAG_NAME, "h3")
                title = title_element.text
                
                # Extract link
                link_element = result.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                
                # Try to extract snippet/description
                snippet = ""
                try:
                    # Multiple possible selectors for description
                    snippet_selectors = [
                        "div.VwiC3b",
                        "div.lyLwlc",
                        "span.aCOpRe",
                        "div[data-sncf='1']"
                    ]
                    
                    for selector in snippet_selectors:
                        try:
                            snippet_element = result.find_element(By.CSS_SELECTOR, selector)
                            snippet = snippet_element.text
                            if snippet:
                                break
                        except NoSuchElementException:
                            continue
                            
                except Exception:
                    snippet = "No description available"
                
                # Store result
                result_dict = {
                    "position": i + 1,
                    "title": title,
                    "link": link,
                    "snippet": snippet
                }
                results_data.append(result_dict)
                
                # Print result
                print("---")
                print(f"Result {i+1}")
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Snippet: {snippet[:100]}..." if len(snippet) > 100 else f"Snippet: {snippet}")
                
            except NoSuchElementException as e:
                print(f"Could not find element in result {i+1}: {e}")
            except Exception as e:
                print(f"Error parsing result {i+1}: {e}")
        
        print(f"\nSuccessfully scraped {len(results_data)} results!")
        
    except TimeoutException:
        print("Timeout: Page took too long to load or elements not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        if driver:
            driver.quit()
            print("Browser closed.")
    
    return results_data


def save_results_to_file(results, filename="search_results.txt"):
    """
    Saves search results to a text file.
    
    Args:
        results (list): List of result dictionaries.
        filename (str): Output filename.
    """
    if not results:
        print("No results to save.")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("GOOGLE SEARCH RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            for result in results:
                f.write(f"Position: {result['position']}\n")
                f.write(f"Title: {result['title']}\n")
                f.write(f"Link: {result['link']}\n")
                f.write(f"Snippet: {result['snippet']}\n")
                f.write("-" * 80 + "\n\n")
        
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


# --- Run the scraper ---
if __name__ == "__main__":
    # Configuration
    search_query = "Selenium Python"
    number_of_results = 5
    run_headless = False  # Set to True to run without browser window
    
    # Run scraper
    results = scrape_google_results(search_query, num_results=number_of_results, headless=run_headless)
    
    # Optionally save results to file
    if results:
        save_results_to_file(results, filename="google_search_results.txt")
        
        # You can also work with results as data
        print(f"\nTotal results scraped: {len(results)}")
        print(f"First result title: {results[0]['title']}")