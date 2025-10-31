# simple web scrapper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# search query (will be used by the function)
search_query = "python selenium automation"  # Set a default query for clarity


def google_scrape(query):
    """
    Uses Selenium to open a browser, search Google, and scrape the result titles and URLs.
    """
    print(f"--- Starting Google search for: '{query}' ---")

    driver = webdriver.Chrome()
    # driver.maximize_window()

    driver.get("https://www.google.com/")
    time.sleep(4)  # Wait a bit for the page to load

    # 1. Search Google
    try:
        # Find the search box by its 'name' attribute, which is typically 'q'
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)  # Use the passed query
        search_box.send_keys(Keys.RETURN)
        time.sleep(30)  # Wait for search results
    except Exception as e:
        print(f"Error during search: {e}")
        driver.quit()
        return

    # 2. Get Search Results (Links)
    # Use a more reliable CSS selector for search result links
    # This selector targets all <a> tags that are direct children of an <h3> tag within a typical search result block
    result_links_elements = driver.find_elements(By.CSS_SELECTOR, "div#search a h3")

    # 3. Iterate Through Results
    print(f"Found {len(result_links_elements)} results. Scraping up to 3.")

    # Iterate through the first 3 results (or fewer if less than 3 are found)
    for i in range(min(3, len(result_links_elements))):
        try:
            # Re-locate the elements in each iteration because page navigation invalidates old WebElements
            # Find all links again to ensure we are working with current elements
            current_links = driver.find_elements(By.CSS_SELECTOR, "div#search a h3")

            # The h3 is a child of the <a> tag that holds the URL.
            # We need to get the parent <a> element to get the 'href'.
            # We use a robust way to get the parent link element (the <a> tag)
            link_element = current_links[i].find_element(By.XPATH, "./ancestor::a[1]")
            href = link_element.get_attribute("href")

            if href:
                print(f"\n--- Result {i + 1} ---")
                print(f"Title: {current_links[i].text}")
                print(f"URL: {href}")

                # Navigate to the result URL
                driver.get(href)
                time.sleep(4)

                print("Page Title:", driver.title)
                # Navigate back to the Google search results page
                driver.back()
                time.sleep(4)

            else:
                print(f"Result {i + 1} link has no href.")

        except Exception as e:
            print(f"An error occurred while processing result {i + 1}: {e}")
            # Ensure we navigate back to continue with the next result if an error occurs
            try:
                driver.back()
                time.sleep(4)
            except:
                pass  # Ignore if navigation fails

    # 5. Close the browser
    driver.quit()
    print("--- Search finished and browser closed. ---")


# Execute the function
google_scrape(search_query)
