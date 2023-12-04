import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# the path to the ChromeDriver executable
CHROME_DRIVER_PATH = "/Users/sarvagyasamridhsingh/Documents/Programming/conda3/python selenium/chromedriver-mac-arm64/chromedriver"

# the directory to save the CSV file
SAVE_DIRECTORY = "/Users/sarvagyasamridhsingh/Documents/INTERNSHIP/internshala/gocargooo"

# Create Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(executable_path=CHROME_DRIVER_PATH), options=chrome_options)

# Open Google 
driver.get("https://www.google.com")

# Find the search box element and enter "Internshala"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Internshala")
search_box.send_keys(Keys.RETURN)

# Wait for a while to ensure the results are loaded
driver.implicitly_wait(5)

# Get all search result elements
search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

# Create a CSV file and write header
csv_file_path = f"{SAVE_DIRECTORY}/google_search_results.csv"
with open(csv_file_path, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["Title", "URL", "Description"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Write search results to CSV
    for result in search_results:
        title = result.find_element(By.CSS_SELECTOR, "h3").text
        url = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        description = result.find_element(By.CSS_SELECTOR, "div span").text

        writer.writerow({"Title": title, "URL": url, "Description": description})

driver.quit()

print(f"Search results exported to {csv_file_path}")
