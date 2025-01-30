from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
def scrapedata(search):

    driver = webdriver.Chrome()

    driver.get("https://www.google.com")

    search_bar = driver.find_element(By.NAME,"q")
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.RETURN)

    time.sleep(3)

    results = driver.find_elements(By.CSS_SELECTOR,"div.tF2Cxc")
    data = []
    for result in results[:10]:
        title = result.find_element(By.TAG_NAME,"h3").text
        link = result.find_element(By.TAG_NAME,"a").get_attribute("href")
        data.append([title,link])
    driver.quit()
    return data
def save_csv(csv_filename,data):
    with open(csv_filename,"w",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title","Link"])
        writer.writerows(data)
    print(f"Top 10 search results saved to {csv_filename}")
if __name__=="__main__":
    search_term = input("Enter the search term: ")
    file_name = input("Enter the filename for the csv file you want to save the data in: ")
    data = scrapedata(search_term)
    if data:
        save_csv(file_name,data)
    else:
        print("No results found.")
