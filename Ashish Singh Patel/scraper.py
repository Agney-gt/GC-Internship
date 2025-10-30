from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
# comment this if you want visible browser
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.google.com")

    # Handle consent popup (for EU or new accounts)
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]"))
        )
        consent_btn.click()
    except:
        pass

    # Perform search
    query = "internship opportunities 2025"
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Flexible wait: for any main result container
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@data-sokoban-container or @class='g' or contains(@class,'tF2C')]")
        )
    )

    # Gather all result titles + links
    result_blocks = driver.find_elements(By.XPATH, "//div[@data-sokoban-container or @class='g' or contains(@class,'tF2C')]")

    print(f"\n🔍 Top Google search results for '{query}':\n")

    count = 0
    for block in result_blocks:
        try:
            title = block.find_element(By.TAG_NAME, "h3").text
            link = block.find_element(By.TAG_NAME, "a").get_attribute("href")
            if title and link:
                count += 1
                print(f"{count}. {title}\n   🔗 {link}\n")
            if count >= 10:
                break
        except:
            continue

    if count == 0:
        driver.save_screenshot("no_results.png")
        print("⚠️ No results detected — saved screenshot as 'no_results.png' for debugging.")

finally:
    driver.quit()
