import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup # The new, unique component

class HybridDataSurveyor:
    def __init__(self, query: str, scrolls: int = 3, headless: bool = True):
        """Initializes the browser and configures options for stability and stealth."""
        
        self.query = query
        self.scrolls = scrolls
        self.results = []
        
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        # Adding a common user-agent for less suspicion
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        print("[INFO]: Setting up Chrome WebDriver.")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def load_and_scroll(self):
        """Loads the Google search page and scrolls to load dynamic content."""
        
        search_url = f"https://www.google.com/search?q={self.query}"
        self.driver.get(search_url)
        print(f"[INFO]: Page loaded for query: '{self.query}'.")

        for i in range(self.scrolls):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3) # Wait for content to load
            print(f"[INFO]: Completed scroll {i + 1}/{self.scrolls}.")

    def parse_with_beautifulsoup(self):
        """Unique Step: Passes the loaded, dynamic HTML source to BeautifulSoup for robust parsing."""
        
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        
        # Abstract Selector Strategy: Searching for elements that contain <h3> tags (titles)
        # We rely on the <div data-hveid> or similar parent tags which usually wrap organic results.
        # This is a less brittle approach than guessing the current MjjYud or Ww4FFb class.
        
        # Targeting the main content area (often the 'search' role or a large div)
        main_content = soup.find('div', {'id': 'rso'}) 
        if not main_content:
            print("[WARNING]: Could not find the main results container (#rso). Using the whole body.")
            main_content = soup.body

        # Find all <h3> tags, which almost always contain the result title
        for h3_tag in main_content.find_all('h3'):
            try:
                # The link (URL) is typically in the parent <a> tag of the <h3> or a nearby ancestor.
                # We climb up to the first <a> ancestor of the <h3>
                link_tag = h3_tag.find_parent('a', href=True) 
                if not link_tag:
                    # Fallback: Look for a link tag near the h3 tag's parent
                    link_tag = h3_tag.find_next_sibling('a', href=True)

                if link_tag:
                    title = h3_tag.text
                    url = link_tag['href']
                    
                    # Search for the description (snippet) text, which is typically near the link.
                    # We look for a sibling element that has a common snippet structure.
                    # This targets the <div class="VwiC3b"> element (or similar)
                    
                    # Find the nearest common container to both the title/link and the snippet
                    result_container = h3_tag.find_parent('div', class_=lambda x: x and ('g' in x or 'MjjYud' in x))
                    
                    description = "N/A"
                    if result_container:
                        # Look for a text-holding div that is not a title or link
                        snippet_div = result_container.find('div', class_=lambda x: x and ('VwiC3b' in x or 'MUxGbd' in x))
                        if snippet_div:
                            description = snippet_div.text.strip()
                    
                    self.results.append({
                        "Title": title,
                        "URL": url,
                        "Description": description
                    })

            except Exception as e:
                # Skip elements that don't conform to the expected structure
                print(f"[WARNING]: Skipping element due to parsing error: {e}")

        print(f"[INFO]: Successfully parsed {len(self.results)} complete results.")


    def save_and_close(self, file_name: str = "hybrid_survey_results.csv"):
        """Saves results and cleanly closes the browser."""
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(file_name, index=False)
            print(f"[INFO]: Results saved to {file_name}.")
        
        self.driver.quit()
        print("[INFO]: Browser closed. Task completed.")

    def run(self):
        """Executes the complete scraping workflow."""
        try:
            self.load_and_scroll()
            self.parse_with_beautifulsoup()
        except Exception as e:
            print(f"[ERROR]: An unexpected critical error occurred: {e}")
        finally:
            # Ensure browser is always closed
            self.save_and_close() 

if __name__ == "__main__":
    print("[INFO]: Starting the Hybrid Data Surveyor...")
    
    # Example usage - feel free to change the query and scrolls
    surveyor = HybridDataSurveyor(query="future of AI in web scraping", scrolls=5, headless=False) 
    surveyor.run()