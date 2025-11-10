from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_google_results(query, num_results=10):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    results = []

    try:
        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )

        titles = driver.find_elements(By.CSS_SELECTOR, "h3")

        for t in titles[:num_results]:
            try:
                parent = t.find_element(By.XPATH, ".//ancestor::a")
                title = t.text
                link = parent.get_attribute("href")
                results.append({"title": title, "link": link})
            except:
                pass
    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    query = input("Enter search query: ")
    results = scrape_google_results(query)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}\n   {result['link']}")
