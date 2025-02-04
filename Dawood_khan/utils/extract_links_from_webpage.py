from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.url_utils import url_split


def get_links(text, website_full_url):
    """
    Get the local links and their frequency in a webpage
    :param text: response.text
    :param website_full_url: homepage of website which is being scraped
    """

    local_urls = list()
    foreign_urls = list()

    base = url_split(website_full_url)["base"]
    strip_base = url_split(website_full_url)["strip_base"]
    base_url = url_split(website_full_url)["base_url"]
    path = url_split(website_full_url)["path"]
    scheme = url_split(website_full_url)["scheme"]

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Running headless browser for scraping
    options.add_argument('--disable-gpu')

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(website_full_url)
    except Exception as e:
        print(f"Error while accessing {website_full_url}: {e}")
        return {}

    # Extract all links using Selenium
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        anchor = link.get_attribute('href')
        if not anchor:
            continue

        anchor = anchor.strip()
        if anchor.startswith('//'):
            endchar = anchor[-1] if anchor.endswith("/") else ""
            anchor = anchor.strip("/") + endchar
        if anchor.startswith('javascript'): continue
        if ("#" in anchor or anchor.startswith("mailto:")
                or anchor.startswith("tel:")):
            continue
        elif anchor.startswith('/'):
            local_link = base_url + anchor
            local_urls.append(local_link)
        elif anchor.startswith("http") and strip_base.lower() in anchor[
                        :anchor.find("/", anchor.find("//") + 2)].lower():
            local_urls.append(anchor)
        elif strip_base.lower() in anchor[:anchor.find("/")].lower():
            local_link = "{}://{}".format(scheme, anchor)
            local_urls.append(local_link)
        elif not anchor.lower().startswith("http"):
            local_link = path + anchor
            local_urls.append(local_link)
        else:
            foreign_urls.append(anchor)

    driver.quit()  # Close the browser

    return dict(Counter(local_urls))


if __name__ == '__main__':
    # get_links(text, website_full_url)
    pass
