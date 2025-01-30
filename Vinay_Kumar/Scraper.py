import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#search query
query = input("Enter your search query: ")

driver = webdriver.Chrome()

try:
    # Opening Google
    driver.get("https://www.google.com")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(18)

    result_titles = driver.find_elements(By.CLASS_NAME, "LC20lb")
    result_links = driver.find_elements(By.CLASS_NAME, "yuRUbf")
    
    search_data = []
    for index in range(min(10, len(result_titles))):  #taking top 10 results
        title = result_titles[index].text
        link = result_links[index].find_element(By.TAG_NAME, "a").get_attribute("href")
        search_data.append([index + 1, title, link])
    
    filename = f"googleSearchResult_{query.replace(' ', '_')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Title", "URL"])
        writer.writerows(search_data)

    print(f"Search results saved to '{filename}'.")

finally:
    # Closing the browser
    driver.quit()
