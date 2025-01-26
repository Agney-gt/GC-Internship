from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def google_search(query):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # Optional: Avoid sandboxing issues

    # Initialize ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")  # Open Google

    # Find the search input box and enter the query
    try:
        search_box = driver.find_element("name", "q")  # Locate search bar by "name"
        search_box.send_keys(query)  # Enter the search query
        search_box.send_keys(Keys.RETURN)  # Simulate pressing "Enter"

        # Wait for user to manually quit
        input("Browser is open. Press Enter to close...")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()  # Close the browser window when the user exits

if __name__ == "__main__":
    query = input("Enter your search query: ")
    google_search(query)
