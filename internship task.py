#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


# In[2]:


# Set up the Chrome WebDriver with the path to your chromedriver executable
chrome_driver_path = r"C:\Users\latap\Downloads\chromedriver-win64.zip\chromedriver.exe"


# In[3]:


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  
chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")


# In[4]:


# Pass the options to the webdriver.Chrome constructor
driver = webdriver.Chrome(options=chrome_options)


# In[5]:


# Open Google and search for the keyword "Internshala"
driver.get("https://www.google.com/")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Internshala")
search_box.send_keys(Keys.RETURN)


# In[6]:


# Wait for the search results to load
driver.implicitly_wait(5)


# In[7]:


# Get search result details and store them in a CSV file
results = driver.find_elements(By.XPATH, '//div[@class="tF2Cxc"]')
csv_data = []

for result in results:
    try:
        title = result.find_element(By.XPATH, './/h3').text
    except:
        title = ""

    try:
        url = result.find_element(By.XPATH, './/a').get_attribute("href")
    except:
        url = ""

    try:
        description = result.find_element(By.XPATH, './/div[@class="IsZvec"]').text
    except:
        description = ""

    csv_data.append([title, url, description])


# In[8]:


# Save data to a CSV file
csv_file_path = "search_results.csv"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Title", "URL", "Description"])  # CSV header
    csv_writer.writerows(csv_data)


# In[9]:


# Close the browser
driver.quit()

print(f"Search results saved to {csv_file_path}")


# In[10]:


import pandas as pd
df = pd.read_csv(csv_file_path)


# In[11]:


df.head()


# In[ ]:




