import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def initialize_driver():
    """
    Initializes and returns a Selenium WebDriver instance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for performance
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver

def perform_google_search(driver, query):
    """
    Performs a Google search using Selenium and returns the search result elements.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        query (str): Search query.

    Returns:
        list: A list of search result titles.
    """
    driver.get("https://www.google.com")

    try:
        # Wait until the search box is available
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Enter the query and submit
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//h3"))
        )

        # Extract search result titles
        results = driver.find_elements(By.XPATH, "//h3")
        return [result.text for result in results if result.text]

    except TimeoutException:
        print("Timed out waiting for page elements to load.")
        return []

def main():
    """
    Main function to execute the Google search scraper.
    """
    driver = initialize_driver()

    try:
        query = "Selenium Python tutorial"
        print(f"Performing Google search for: '{query}'")

        search_results = perform_google_search(driver, query)

        print("\nTop Search Results:")
        for index, result in enumerate(search_results[:10], start=1):  # Limit to top 10 results
            print(f"{index}. {result}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
