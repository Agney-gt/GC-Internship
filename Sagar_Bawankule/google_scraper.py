"""Google Search Scraper using Selenium with XPath"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def setup_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def scrape_google(query, num_results=10, headless=False):
    driver = setup_driver(headless)
    results = []
    
    try:
        print("Opening Google...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        print("Searching...")
        try:
            search_box = driver.find_element(By.XPATH, "//textarea[@name='q']")
        except:
            search_box = driver.find_element(By.XPATH, "//input[@name='q']")
        
        search_box.send_keys(query)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        
        print("Extracting results...")
        count = 0
        i = 1
        while count < num_results:
            try:
                base = f"(//div[contains(@class, 'g') and .//h3])[{i}]"
                title = driver.find_element(By.XPATH, f"{base}//h3").text
                
                # Skip if title is empty
                if not title or title.strip() == "":
                    i += 1
                    continue
                
                url = driver.find_element(By.XPATH, f"{base}//a[@href]").get_attribute("href")
                
                try:
                    desc = driver.find_element(By.XPATH, f"{base}//div[contains(@class, 'VwiC3b')]").text
                except:
                    desc = "N/A"
                
                count += 1
                results.append({'rank': count, 'title': title, 'url': url, 'description': desc})
                print(f"{count}. {title}")
                i += 1
                
            except Exception as e:
                # Try next element
                i += 1
                if i > num_results + 20:  # Stop after trying 20 extra elements
                    print(f"Stopped searching after {i} attempts")
                    break
        
        print(f"\n✓ Scraped {len(results)} results")
        print("Browser will remain open. Press Ctrl+C in terminal to exit.")
        
        # Keep the browser open indefinitely
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n\nClosing browser...")
        driver.quit()
    except Exception as e:
        print(f"Error: {e}")
        print("Browser will remain open. Press Ctrl+C in terminal to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nClosing browser...")
            driver.quit()
    
    return results


def main():
    query = input("Search query: ")
    num = int(input("Number of results (10): ") or "10")
    
    results = scrape_google(query, num)
    
    if results:
        print("\n" + "="*70)
        for r in results:
            print(f"{r['rank']}. {r['title']}\n   {r['url']}\n")
        print("="*70)
    else:
        print("\nNo results found!")


if __name__ == "__main__":
    main()