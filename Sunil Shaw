import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class GetSearchResults:
    
    def __init__(self,query: str,n_scrolls: int = 5) -> None:        
        self.driver = Chrome()
        self.url = []
        self.description = []
        self.title = []
        self.driver.get(f'https://www.google.com/search?q={query}')
        print('[INFO]: connection established')
        
        for _ in range(n_scrolls):
            self._scroll_page()
        
        self._extract_info()
        
    def _scroll_page(self):
        body = self.driver.find_element(By.TAG_NAME,value="body")
        body.send_keys(Keys.END)
        time.sleep(2)

    def _extract_info(self):
        self.results = self.driver.find_element(By.ID, value='main')
        html_elements = self.results.find_elements(By.CLASS_NAME,value='MjjYud')
        
        for element in html_elements:
            try:
                heading = element.find_element(By.CSS_SELECTOR,value="h3.LC20lb.MBeuO.DKV0Md")
                des = element.find_element(By.CSS_SELECTOR,value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
                link = element.find_element(By.CSS_SELECTOR,value="a").get_attribute('href')
                self.title.append(heading.text)
                self.description.append(des.text)
                self.url.append(link)

            except Exception as e:
                pass
            
        print('[INFO]: information extracted')
        self.driver.quit()
        print('[INFO]: closing connection')
            
    def to_csv(self,file_path):
        self.data_dict = {
            'Title': self.title,
            'Description': self.description,
            'URL': self.url
        }
        dataframe = pd.DataFrame(data=self.data_dict)
        dataframe.to_csv(file_path,index=False)
        print('[INFO]: csv file created')
        
if __name__ == '__main__':
    query = 'Internshala'
    obj = GetSearchResults(query)
    obj.to_csv('./search_result.csv')
    
    
