from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def scrape_google_with_snippets(query, max_results=10, headless=False):
    """
    Enhanced Google scraper that also extracts snippets/descriptions
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(10)

    try:
        print(f"Searching for: {query}")
        driver.get("https://www.google.com")
        time.sleep(1)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # wait for results

        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        output = []
        
        for idx, result in enumerate(results[:max_results], start=1):
            try:
                # Extract title
                title_elem = result.find_element(By.CSS_SELECTOR, "h3")
                title = title_elem.text
            except NoSuchElementException:
                title = "No title found"
            
            try:
                # Extract link
                link_elem = result.find_element(By.TAG_NAME, "a")
                link = link_elem.get_attribute("href")
            except NoSuchElementException:
                link = "No link found"
                
            try:
                # Extract snippet (description)
                snippet_elem = result.find_element(By.CSS_SELECTOR, "span")
                snippet = snippet_elem.text
            except NoSuchElementException:
                snippet = "No description available"

            output.append({
                "rank": idx,
                "title": title,
                "link": link,
                "snippet": snippet
            })

        return output

    except TimeoutException:
        print("Page load timeout occurred")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()

def save_results_to_file(results, filename="search_results.txt"):
    """
    Save search results to a text file
    """
    with open(filename, "w", encoding="utf-8") as f:
        for result in results:
            f.write(f"Rank: {result['rank']}\n")
            f.write(f"Title: {result['title']}\n")
            f.write(f"Link: {result['link']}\n")
            f.write(f"Snippet: {result['snippet']}\n")
            f.write("-" * 50 + "\n\n")
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    query = "Python web scraping"
    results = scrape_google_with_snippets(query, max_results=5, headless=False)
    
    if results:
        print(f"\nTop results for '{query}':\n")
        for result in results:
            print(f"{result['rank']}. {result['title']}")
            print(f"   {result['link']}")
            print(f"   Description: {result['snippet'][:100]}...")
            print()
        
        # Save results to file
        save_results_to_file(results, f"{query.replace(' ', '_')}_results.txt")
    else:
        print("No results found or an error occurred.")