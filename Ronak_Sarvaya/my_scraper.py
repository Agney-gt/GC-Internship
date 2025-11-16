"""
Google Search Scraper using Selenium
Author: Ronak Sarvaya
Description: Scrapes Google search results including title, URL, and snippet
"""

import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class GoogleScraper:
    """A class to scrape Google search results using Selenium"""
    
    def __init__(self, headless=True):
        """
        Initialize the Google Scraper
        
        Args:
            headless (bool): Run browser in headless mode (default: True)
        """
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent to avoid detection
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        try:
            # Initialize driver with webdriver_manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            print("✅ Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Chrome WebDriver: {e}")
            print("\n💡 Troubleshooting tips:")
            print("1. Make sure Google Chrome is installed")
            print("2. Try updating Chrome to the latest version")
            print("3. Run: pip install --upgrade selenium webdriver-manager")
            raise
        
    def search_google(self, query):
        """
        Perform a Google search
        
        Args:
            query (str): Search query string
        """
        try:
            # Navigate to Google
            self.driver.get("https://www.google.com")
            print(f"🔍 Searching Google for: '{query}'")
            
            # Wait for search box and handle cookie consent if present
            try:
                # Try to click "Accept all" button if it appears
                accept_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree')]"))
                )
                accept_button.click()
                time.sleep(1)
            except:
                pass  # No cookie consent or already accepted
            
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Enter search query
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            print("✅ Search completed successfully")
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            raise
            
    def extract_results(self, num_results=10):
        """
        Extract search results from the page
        
        Args:
            num_results (int): Maximum number of results to extract
            
        Returns:
            list: List of dictionaries containing search results
        """
        results = []
        
        try:
            # Wait a bit for all results to load
            time.sleep(3)
            
            # Try multiple CSS selectors for search results
            search_results = []
            selectors = [
                "div.g",
                "div[data-sokoban-container]",
                "div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe",
                "div[jscontroller][data-hveid]"
            ]
            
            for selector in selectors:
                search_results = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(search_results) > 0:
                    print(f"📊 Found {len(search_results)} search results using selector: {selector}")
                    break
            
            if len(search_results) == 0:
                print("⚠️ No search results found with any selector")
                # Save screenshot for debugging
                try:
                    self.driver.save_screenshot("debug_screenshot.png")
                    print("📸 Screenshot saved as debug_screenshot.png")
                except:
                    pass
                return results
            
            for i, result in enumerate(search_results[:num_results]):
                try:
                    # Extract title - try multiple selectors
                    title = None
                    title_selectors = ["h3", "div[role='heading']", ".LC20lb"]
                    for sel in title_selectors:
                        try:
                            title_element = result.find_element(By.CSS_SELECTOR, sel)
                            title = title_element.text
                            if title:
                                break
                        except:
                            continue
                    
                    if not title:
                        continue
                    
                    # Extract URL
                    url = None
                    try:
                        url_element = result.find_element(By.CSS_SELECTOR, "a")
                        url = url_element.get_attribute("href")
                    except:
                        continue
                    
                    # Extract snippet/description - try multiple selectors
                    snippet = "No description available"
                    snippet_selectors = [
                        "div[data-sncf='1']",
                        "div.VwiC3b",
                        "div.IsZvec",
                        "span.aCOpRe",
                        "div[style*='-webkit-line-clamp']"
                    ]
                    for sel in snippet_selectors:
                        try:
                            snippet_element = result.find_element(By.CSS_SELECTOR, sel)
                            snippet = snippet_element.text
                            if snippet:
                                break
                        except:
                            continue
                    
                    # Only add if we have valid data
                    if title and url and url.startswith("http"):
                        results.append({
                            "rank": len(results) + 1,
                            "title": title,
                            "url": url,
                            "snippet": snippet
                        })
                        
                        print(f"✓ Extracted result #{len(results)}: {title[:50]}...")
                        
                except Exception as e:
                    print(f"⚠️ Could not extract result: {e}")
                    continue
            
            print(f"✅ Successfully extracted {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Error extracting results: {e}")
            return results
            
    def save_to_csv(self, results, query, filename=None):
        """
        Save results to CSV file
        
        Args:
            results (list): List of result dictionaries
            query (str): Search query used
            filename (str): Output filename (optional)
        """
        if not results:
            print("⚠️ No results to save")
            return
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_results_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['rank', 'title', 'url', 'snippet']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(results)
            
            print(f"✅ Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")
            
    def scrape(self, query, num_results=10, save_csv=True):
        """
        Main method to scrape Google search results
        
        Args:
            query (str): Search query
            num_results (int): Number of results to extract
            save_csv (bool): Whether to save results to CSV
            
        Returns:
            list: List of search results
        """
        try:
            self.setup_driver()
            self.search_google(query)
            results = self.extract_results(num_results)
            
            if save_csv and results:
                self.save_to_csv(results, query)
            
            return results
            
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            return []
            
        finally:
            self.close()


def main():
    """Main function to demonstrate the scraper"""
    print("=" * 60)
    print("Google Search Scraper - Ronak Sarvaya")
    print("=" * 60)
    
    # Configuration
    SEARCH_QUERY = "Python programming tutorials"
    NUM_RESULTS = 10
    HEADLESS_MODE = False  # Set to False to see the browser
    
    # Create scraper instance
    scraper = GoogleScraper(headless=HEADLESS_MODE)
    
    # Perform scraping
    results = scraper.scrape(
        query=SEARCH_QUERY,
        num_results=NUM_RESULTS,
        save_csv=True
    )
    
    # Display results
    if results:
        print("\n" + "=" * 60)
        print("SEARCH RESULTS")
        print("=" * 60)
        
        for result in results:
            print(f"\n[{result['rank']}] {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Snippet: {result['snippet'][:100]}...")
            print("-" * 60)
    else:
        print("\n⚠️ No results found or scraping failed")
    
    print("\n✅ Scraping completed!")


if __name__ == "__main__":
    main()
