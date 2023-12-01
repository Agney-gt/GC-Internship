# Importing necessary libraries
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import time
import pandas as pd
from helpers import log_info, log_error


# Class definition for Google Search Automation
class GoogleSearchAutomation:
    def __init__(self, driver_path):
        # Initializing the webdriver
        self.driver = Chrome(executable_path=driver_path)
        # Initializing an empty DataFrame to store the search results
        self.dataset = pd.DataFrame(
            columns=["Official_site", "Url_title", "Url", "Description"]
        )

    def search_for_query(self, query):
        # Navigating to the Google homepage
        self.driver.get("https://www.google.com")
        # Search the input field
        search_field = self.driver.find_element(By.NAME, "q")
        search_field.send_keys(query)
        # submitting the search query
        search_field.submit()
        # Adding a wait to ensure the page loads before proceeding
        self.driver.implicitly_wait(2)

    # Function for loading all contents
    def scroll_to_bottom(self):
        # initlize the height to zero
        old_scroll_height = 0
        while True:
            # Scrolling to the bottom of the page
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)
            try:
                # handling exceptions
                # Checking if there is more search results
                element = self.driver.find_element(By.CSS_SELECTOR, ".WZH4jc.w7LJsc")
                element.click()
            except Exception:
                continue

            # generating the new scroll height
            new_scroll_height = self.driver.execute_script(
                "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
            )

            # Checking if the scroll height has not changed
            if new_scroll_height == old_scroll_height:
                break
            else:
                old_scroll_height = new_scroll_height

    # Function to extract the search results
    def extract_data_from_results(self):
        frames = self.driver.find_elements(By.CLASS_NAME, "tF2Cxc")
        for f in frames:
            try:
                official_site = f.find_element(By.CLASS_NAME, "VuuXrf").text
            except Exception:
                official_site = None

            try:
                url = f.find_element(
                    By.CSS_SELECTOR, "[jsname='UWckNb']"
                ).get_attribute("href")
            except Exception:
                url = None

            try:
                link_title = f.find_element(By.TAG_NAME, "h3").text
            except Exception:
                link_title = None

            try:
                description = f.find_element(
                    By.CSS_SELECTOR, "div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf"
                ).text
            except Exception:
                description = None

            self.dataset.loc[len(self.dataset)] = [
                official_site,
                link_title,
                url,
                description,
            ]

        self.driver.quit()

        return self.dataset


if __name__ == "__main__":
    log_info("Google Search Automation started.")

    # Creating an instance of the GoogleSearchAutomation class
    google_automation = GoogleSearchAutomation(
        "/home/rahuldevs/chromedriver_linux64/chromedriver"
    )
    try:
        # Performing a Google search for "Internshala"
        google_automation.search_for_query("Internshala")
        # Scrolling to the bottom of the search results page
        google_automation.scroll_to_bottom()
        # Extracting data from the search results and saving it to a CSV file
        extracted_data = google_automation.extract_data_from_results()
        extracted_data.to_csv("search_result.csv")
        log_info("Google Search Automation completed successfully.")
    except Exception as e:
        log_error(f"Error during Google Search Automation: {str(e)}")
    finally:
        google_automation.driver.quit()
