# Internship Assignment Submition - Data Scrapper

This project allows you to scrape websites and extract both **internal** and **external** links using **Selenium** and **BeautifulSoup**. It is designed to crawl websites, follow internal links, and store the extracted data in **JSON** format. The scraper uses **proxy rotation** and **user agent rotation** to avoid detection and bypass common anti-bot mechanisms.

## Features

- **Proxy Rotation**: Utilizes proxies to rotate IP addresses, avoiding IP bans and restrictions.
- **User Agent Rotation**: Simulates requests from different browsers by rotating user agents, helping to avoid detection as a bot.
- **Crawling**: The scraper follows internal links recursively, extracting relevant links while ignoring unwanted or non-local URLs.
- **Redis Integration**: Efficiently manages visited and unvisited URLs using Redis, ensuring the scraper doesn’t revisit previously crawled pages.
- **Selenium for JavaScript Rendering**: Supports websites that load content dynamically via JavaScript by using Selenium to execute JavaScript and retrieve fully rendered pages.

## Requirements

- Python 3.10+
- `pip` for installing dependencies
- **Redis** (for URL storage)

### Setting Up the Environment

1. **Create and Activate a Virtual Environment:**

    For Unix/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    For Windows:
    ```bash
    python3 -m venv venv
    venv\Scripts\activate
    ```

2. **Install the Required Dependencies:**

    After activating your virtual environment, install the project dependencies using:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install Redis** (if not already installed):
    - Follow the [Redis installation guide](https://redis.io/docs/getting-started/) to install and start Redis on your machine.

## Usage

### Starting the Scraper

To start the web scraper, run the following command in your terminal:

```bash
python -m webscraper <website_url> --start_afresh <True or False>
```

- **Replace `<website_url>`** with the URL of the website you wish to scrape (e.g., `https://internshala.com/internships/`).
- **`--start_afresh`**: If set to `True`, the scraper will clear the Redis database and start from the given URL. Default is `True`.

### Arguments

- **`website_url`**: The URL of the website to scrape.
- **`--start_afresh`**: If `True`, the Redis database is cleared and the scraper starts from the provided URL. Default is `True`.

### How It Works

1. **Proxy Rotation**:
    - Proxies are fetched from a proxy provider and stored in a list.
    - Each request is made using a random proxy to prevent IP bans.

2. **User Agent Rotation**:
    - Random user agents are used for each request to simulate different browsers and avoid detection.

3. **Request Handling**:
    - The scraper handles both HTTP and HTTPS links that are internal to the target website.

4. **Link Extraction**:
    - **BeautifulSoup** parses the HTML to extract all links.
    - **Selenium** is used to handle pages that require JavaScript execution for content rendering (e.g., dynamic content loading).

5. **Redis Storage**:
    - Redis stores processed URLs to prevent revisiting.
    - New URLs are dynamically added to Redis for further crawling.

6. **Data Storage**:
    - The HTML content of the pages is stored in **JSON** files for later analysis.

## Known Issues

- **ChromeDriver Compatibility**: Ensure that you have a compatible version of **ChromeDriver** installed on your system for Selenium to work properly. The script will attempt to automatically download the correct driver using `webdriver-manager`.
- **CAPTCHA and Anti-Bot Mechanisms**: The scraper may not be able to bypass advanced CAPTCHAs or sophisticated anti-bot systems. You may need additional configuration or third-party services (e.g., CAPTCHA solving) for such websites.
