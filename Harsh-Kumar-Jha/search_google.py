import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs


def clean_url(url):
    """Remove Google redirect wrapper"""
    if 'google.com/url?q=' in url:
        return parse_qs(urlparse(url).query).get('q', [url])[0]
    return url


def scrape_google(query):
    # Setup with stealth options
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
    })
    
    print(f"🔍 Searching: {query}\n")
    results = []
    
    try:
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # Handle cookie popup
        try:
            driver.find_element(By.XPATH, "//button[contains(., 'Reject') or contains(., 'Accept')]").click()
            time.sleep(1)
        except:
            pass
        
        # Search
        driver.find_element(By.NAME, "q").send_keys(query + Keys.RETURN)
        time.sleep(5)
        
        # BETTER APPROACH: Find all h3 elements (more reliable)
        h3_elements = driver.find_elements(By.TAG_NAME, "h3")
        print(f"Debug: Found {len(h3_elements)} h3 elements\n")
        
        for h3 in h3_elements:
            try:
                # Get title
                title = h3.text.strip()
                if not title:
                    continue
                
                # Get URL from parent anchor tag
                try:
                    link = h3.find_element(By.XPATH, "./ancestor::a[1]").get_attribute("href")
                    url = clean_url(link)
                except:
                    continue
                
                # Skip Google's own links
                if "google.com" in url:
                    continue
                
                # Get description - find the parent search result div
                description = ""
                try:
                    # Navigate up to find the search result container
                    parent = h3.find_element(By.XPATH, "./ancestor::div[@class='g' or @data-hveid or @data-sokoban-container][1]")
                    
                    # Look for description text
                    desc_elements = parent.find_elements(By.XPATH, 
                        ".//div[contains(@class, 'VwiC3b')] | "
                        ".//div[contains(@class, 'IsZvec')] | "
                        ".//div[@data-sncf] | "
                        ".//em/parent::*/parent::* | "
                        ".//span[@class='st']"
                    )
                    
                    if desc_elements:
                        # Get text and clean it
                        desc_text = desc_elements[0].text.strip()
                        # Remove title if it appears in description
                        if title in desc_text:
                            desc_text = desc_text.replace(title, "").strip()
                        description = desc_text[:300]  # Limit to 300 chars
                    
                    # Fallback: Get any text from parent that's not the title
                    if not description:
                        all_text = parent.text
                        description = all_text.replace(title, "").replace(url, "").strip()[:300]
                        
                except Exception as e:
                    description = "No description available"
                
                # Add to results
                print(f"[{len(results)+1}] {title}")
                print(f"    URL: {url}")
                print(f"    DESC: {description}\n")
                
                results.append({
                    'title': title,
                    'url': url,
                    'description': description
                })
                
                # Stop after 5 results
                if len(results) >= 5:
                    break
                    
            except Exception as e:
                continue
                
    finally:
        driver.quit()
        
    return results


if __name__ == "__main__":
    results = scrape_google("Software Engineering")
    print(f"{'='*70}")
    print(f"✅ Extracted {len(results)} results with full metadata")
