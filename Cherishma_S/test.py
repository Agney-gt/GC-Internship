from selenium import webdriver

driver = webdriver.Chrome()  # Uses ChromeDriver
driver.get("https://www.google.com")
print("ChromeDriver is working!")
driver.quit()
