import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def human_like_delay(min_delay=1, max_delay=3):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def solve_captcha(api_key, site_key, url):
    captcha_url = "http://2captcha.com/in.php"
    params = {
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': site_key,
        'pageurl': url,
    }

    response = requests.post(captcha_url, data=params)
    request_result = response.text

    if 'OK|' not in request_result:
        print(f"Error with 2Captcha request: {request_result}")
        return None

    captcha_id = request_result.split('|')[1]

    solution_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
    for _ in range(20):
        time.sleep(5)
        solution_response = requests.get(solution_url)
        if 'OK|' in solution_response.text:
            solution = solution_response.text.split('|')[1]
            return solution
        else:
            print("Captcha not solved yet, retrying...")
    return None

def set_up_driver():
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def scrape_google(query, max_results=10, api_key=None):
    driver = set_up_driver()

    try:
        driver.get("https://www.google.com")
        human_like_delay(2, 5)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        human_like_delay(1, 2)
        search_box.send_keys(Keys.RETURN)
        human_like_delay(2, 3)

        try:
            driver.find_element(By.CSS_SELECTOR, "div.g-recaptcha")
            print("CAPTCHA detected, solving it...")

            site_key = driver.find_element(By.CSS_SELECTOR, "div.g-recaptcha").get_attribute("data-sitekey")
            captcha_solution = solve_captcha(api_key, site_key, driver.current_url)

            if captcha_solution:
                driver.execute_script(
                    f'document.getElementById("g-recaptcha-response").innerHTML="{captcha_solution}";')
                driver.find_element(By.ID, "captcha-submit-button").click()
                human_like_delay(3, 5)
                print("CAPTCHA solved!")
            else:
                print("Failed to solve CAPTCHA.")
                return []

        except Exception as e:
            print(f"No CAPTCHA detected or solved: {e}")

        results = []
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        for result in search_results[:max_results]:
            title = result.find_element(By.TAG_NAME, "h3").text
            url = result.get_attribute("href")
            results.append({"title": title, "url": url})
            human_like_delay(1, 2)

        return results

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    query = input("Enter your search query: ")
    max_results = int(input("Enter the maximum number of results to fetch: "))
    api_key = input("Enter 2Captcha API key: ")

    search_results = scrape_google(query, max_results, api_key)

    if search_results:
        print("\nGoogle Search Results:")
        for i, result in enumerate(search_results, start=1):
            print(f"{i}. {result['title']} ({result['url']})")
    else:
        print("No results found or CAPTCHA was not solved.")
