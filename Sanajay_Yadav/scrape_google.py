import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- This is the search query. We can search for anything. ---
QUERY = "Sanjay Yadav GitHub"

def scrape_google(search_query):
    print(f"Starting scraper for query: '{search_query}'...")

    # Set up the Chrome driver automatically
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run in headless mode (no browser window)
    options.add_argument('--log-level=3') # Suppress console logs
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 1. Go to Google
        driver.get("https://www.google.com")

        # 2. Find the search bar (the 'name' attribute is 'q')
        search_box = driver.find_element(By.NAME, "q")

        # 3. Type in the query and press Enter
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)

        # 4. Wait for 3 seconds for the results to load
        time.sleep(3)

        # 5. Find all the search result elements
        # We find the 'a' tags that contain an 'h3' tag, which is the common structure for a Google result.
        result_elements = driver.find_elements(By.CSS_SELECTOR, "a h3")

        if not result_elements:
            print("No search results found.")
            return

        print(f"--- Found {len(result_elements)} results for '{search_query}' ---")

        # 6. Loop through the results and print the title and link
        for element in result_elements:
            try:
                title = element.text
                # The 'a' tag is the parent of the 'h3'. We go up one level to get the 'href' (the link).
                link = element.find_element(By.XPATH, "..").get_attribute("href")

                # Filter out empty titles or links, and links that are not real results
                if title and link and not link.startswith("https.://www.google.com"):
                    print(f"\nTitle: {title}")
                    print(f"Link: {link}")
            except Exception as e:
                pass # Skip any elements that aren't real search results

        print("\n--- Scraping complete. ---")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # 7. Close the browser
        driver.quit()

# --- Run the scraper ---
if __name__ == "__main__":
    scrape_google(QUERY)