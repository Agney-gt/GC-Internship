
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_quotes():
    """
    Scrapes quotes from quotes.toscrape.com using Selenium.

    Returns:
        A list of dictionaries, where each dictionary contains the quote, author, and tags.
    """
    # Set up the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the website
    driver.get("http://quotes.toscrape.com/")

    # Extract the quotes
    quotes = []
    for quote_element in driver.find_elements(By.CLASS_NAME, "quote"):
        text = quote_element.find_element(By.CLASS_NAME, "text").text
        author = quote_element.find_element(By.CLASS_NAME, "author").text
        tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, "tag")]
        quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    # Close the driver
    driver.quit()

    return quotes

if __name__ == '__main__':
    scraped_data = scrape_quotes()
    for item in scraped_data:
        print(f"Quote: {item['text']}")
        print(f"Author: {item['author']}")
        print(f"Tags: {', '.join(item['tags'])}\n")
