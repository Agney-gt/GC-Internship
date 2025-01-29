from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def google_search(query):
    """
    Performs a Google search using Selenium and prints the top 10 search results.
    """

    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--disable-gpu")  # Disable GPU rendering
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Avoid limited resources in Docker/Linux

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        # Open Google Search
        driver.get("https://www.google.com")

        # Accept Cookies (if prompted)
        try:
            accept_cookies = driver.find_element(By.XPATH, "//button[contains(text(),'Accept all')]")
            accept_cookies.click()
            time.sleep(1)  # Wait for cookie acceptance
        except:
            pass  # No cookie prompt, continue

        # Locate the search bar, enter the query, and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for results to load

        # Extract search result titles and links
        results = driver.find_elements(By.CSS_SELECTOR, "h3")

        print(f"\n🔍 Top 10 search results for '{query}':\n")
        for index, result in enumerate(results[:10]):  # Limit to first 10 results
            try:
                title = result.text
                link = result.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
                print(f"{index + 1}. {title}\n   🔗 {link}\n")
            except:
                continue  # Skip results without valid links

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        driver.quit()  # Close the browser

# Run the script
if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    google_search(search_query)
