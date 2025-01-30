from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time  

driver = webdriver.Chrome(executable_path='path/to/chromedriver')  
driver.get("https://www.google.com")  
 
search_box = driver.find_element("name", "q")  
search_box.send_keys("Selenium Python")  
search_box.send_keys(Keys.RETURN)  
 
time.sleep(2)  
results = driver.find_elements("css selector", "h3")  

for result in results:  
    print(result.text)  

driver.quit()