# proxy_utils/proxy.py
import json
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import HOME_DIR
from utils.user_agent_utils.user_agent import UserAgent

ua = UserAgent()

class Proxy:
    def __init__(self):
        self.proxy_list = self.read_proxy_list()
        if not self.proxy_list:
            self.proxy_list = self.update_proxy_list()
            self.write_proxy_list()
        self.count = 0
        self.proxy = None

    @staticmethod
    def read_proxy_list():
        filename = os.path.join(HOME_DIR, "utils/proxy_utils/proxy_list.json")
        if os.path.exists(filename):
            with open(filename, "r") as fp:
                return json.load(fp)
        return None

    @staticmethod
    def update_proxy_list():
        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Running headless browser for scraping
        options.add_argument('--disable-gpu')
        options.add_argument(f"user-agent={ua.user_agent()}")

        # Initialize Selenium WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        url = 'https://www.sslproxies.org/'
        try:
            driver.get(url)
        except Exception as e:
            raise Exception(f"Could not scrape proxies from {url}! Error: {e}")

        # Find the proxy list table using Selenium
        proxies_table = driver.find_element(By.ID, 'proxylisttable')
        rows = proxies_table.find_elements(By.TAG_NAME, 'tr')

        proxy_list = []
        # Loop through each row and extract proxy details
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) > 1:
                proxy = columns[0].text + ':' + columns[1].text
                proxy_list.append(proxy)

        driver.quit()  # Close the browser

        return proxy_list

    def write_proxy_list(self):
        with open("proxy_list.json", "w") as fp:
            json.dump(self.proxy_list, fp)

    def generate_proxy(self):
        """Choose a random proxy; keeps the same proxy for some number of times then changes it
        """
        if self.count % 10 == 0:
            self.proxy = random.choice(self.proxy_list)
        return {
            "http": self.proxy,
            "https": self.proxy
        }


if __name__ == '__main__':
    pro = Proxy()
    print(pro.generate_proxy())
