from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_google_search(query, num_results=10):
    print(f"\n🔍 Searching Google for: '{query}'")
    print("=" * 60)
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    results_list = []
    
    try:
        driver.get("https://www.google.com")
        time.sleep(3)
        
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        
        if len(results) == 0:
            results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
        
        if len(results) == 0:
            results = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/parent::div")
        
        print(f"\n✅ Found {len(results)} results\n")
        
        if len(results) == 0:
            driver.save_screenshot("debug_screenshot.png")
            print("⚠️ No results found. Screenshot saved.\n")
        
        for index, result in enumerate(results[:num_results], 1):
            try:
                title = ""
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text
                except:
                    try:
                        title = result.find_element(By.CSS_SELECTOR, "h3").text
                    except:
                        continue
                
                link = ""
                try:
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    try:
                        link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    except:
                        continue
                
                description = "No description available"
                try:
                    description = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
                except:
                    try:
                        description = result.find_element(By.CSS_SELECTOR, "div[data-sncf]").text
                    except:
                        pass
                
                if title and link:
                    result_data = {
                        'title': title,
                        'link': link,
                        'description': description
                    }
                    results_list.append(result_data)
                    
                    print(f"{index}. {title}")
                    print(f"   URL: {link}")
                    print(f"   Description: {description[:100]}...")
                    print()
                
            except:
                continue
        
    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error_screenshot.png")
    
    finally:
        time.sleep(3)
        driver.quit()
        print("\n✅ Scraping complete!")
    
    return results_list

if __name__ == "__main__":
    search_query = input("Enter search query: ")
    
    if search_query.strip():
        scrape_google_search(search_query)
    else:
        print("❌ Search query cannot be empty!")