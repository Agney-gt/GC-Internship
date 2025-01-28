from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set the path to your WebDriver
driver_path = '/path/to/chromedriver'  # Update with the path to chromedriver

# Initialize the WebDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Function to scrape Google search results
def scrape_google(query):
    # Open Google
    driver.get('https://www.google.com')
    
    # Find the search box and enter the search query
    search_box = driver.find_element('name', 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for results to load
    time.sleep(2)
    
    # Collect the search result titles and URLs
    results = driver.find_elements('css selector', 'h3')
    
    for result in results:
        title = result.text
        link = result.find_element('xpath', '..').get_attribute('href')
        print(f'Title: {title}\nLink: {link}\n')

# Scrape the search results for a sample query
scrape_google("ChatGPT")

# Close the WebDriver
driver.quit()
