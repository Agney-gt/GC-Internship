import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Function to initialize WebDriver with options
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Uncomment the next line to run with GUI for debugging (Disable headless mode)
    # options.add_argument("--headless=new")  # Comment this line if you want to see the browser

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")

    # Add a User-Agent to avoid bot detection
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to scrape Google search results
def scrape_google_results(query, num_results=10):
    driver = initialize_driver()
    driver.get("https://www.google.com")

    # Find the search box and enter the query
    search_box = driver.find_element(By.CSS_SELECTOR, "textarea[name='q']")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load (increased delay to prevent blocking)
    time.sleep(random.uniform(5, 10))

    results = []

    # Use updated CSS selectors for search results
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")  # New selector for search results

    for result in search_results[:num_results]:
        try:
            title_element = result.find_element(By.CSS_SELECTOR, "h3")
            link_element = result.find_element(By.CSS_SELECTOR, "a")
            snippet_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")  # New selector for description

            title = title_element.text if title_element else "No Title"
            link = link_element.get_attribute("href") if link_element else "No Link"
            snippet = snippet_element.text if snippet_element else "No Description"

            results.append({"Title": title, "Link": link, "Description": snippet})
        except Exception:
            pass  # Ignore errors and continue

    driver.quit()
    return results

# Function to save results to a CSV file
def save_to_csv(data, filename="search_results.csv"):
    if data:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Link", "Description"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Results saved to {filename}")
    else:
        print("No data to save.")

# Main function to run the scraper
if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    scraped_data = scrape_google_results(search_query)

    if scraped_data:
        print("\nTitle\tLink\tDescription")
        for item in scraped_data:
            print(f"{item['Title']}\t{item['Link']}\t{item['Description']}")
        save_to_csv(scraped_data)
    else:
        print("No results found.")
