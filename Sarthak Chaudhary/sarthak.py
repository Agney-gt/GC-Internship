# importing the required libraries
from selenium import webdriver          
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
import time                             

# ask the user what they want to search
search = input("What do you want to search? ")

# open duck duck go
browser = webdriver.Chrome()       
browser.maximize_window()          
browser.get("https://duckduckgo.com")  

# search for something
box = browser.find_element(By.NAME, "q")  
box.send_keys(search)                     
box.send_keys(Keys.ENTER)                 

time.sleep(2)  

links = browser.find_elements(By.CSS_SELECTOR, "a.result__a")

print("\nHere are the top 5 results:\n")

# get first five results
count = 1  
for link in links[:5]:  
    title = link.text  
    url = link.get_attribute("href")  
    print(f"{count}. {title}")  
    print(url, "\n")            
    count += 1                  

time.sleep(3)
browser.quit()
