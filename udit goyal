from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_google_search_results(search_query):
    """
    Scrapes Google search results for a given query.

    Args:
        search_query: The search query to use.

    Returns:
        A list of tuples, where each tuple contains the title and URL of a search result.
    """

    driver = webdriver.Chrome()  # Replace with your preferred browser (e.g., Firefox, Edge)
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.submit()

    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tF2Cxc"))  # Adjust CSS Selector as needed
        )

        search_results = []
        for result in results:
            link = result.find_element(By.TAG_NAME, "a")
            title = link.text
            url = link.get_attribute("href")
            search_results.append((title, url))

    except Exception as e:
        print(f"Error scraping results: {e}")
        search_results = []

    finally:
        driver.quit()
        return search_results

if __name__ == "__main__":
    search_query = "your_search_query"  # Replace with your desired search query
    results = scrape_google_search_results(search_query)

    if results:
        print("Search Results:")
        for title, url in results:
            print(f"Title: {title}")
            print(f"URL: {url}")
            print("-" * 20)
    else:
        print("No results found.")
