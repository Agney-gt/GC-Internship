# Google Search Results Scraper

This is a Python script that uses Selenium to scrape Google search results.

## Requirements

- Python 3.6+
- Selenium package
- Google Chrome browser
- ChromeDriver

## Installation

1. Install the required packages:
   ```
   pip install selenium
   ```

2. Install ChromeDriver:
   - Download from: https://chromedriver.chromium.org/
   - Add to your system PATH

## Usage

Run the script:
```bash
python google_scraper.py
```

The script will search for "Python programming" and display the top 5 search results.

## Code Explanation

The script uses Selenium WebDriver to:
1. Open a headless Chrome browser
2. Navigate to Google
3. Enter a search query
4. Extract search results including:
   - Rank
   - Title
   - URL
   - Snippet (description)

## Note

This is for educational purposes only. Be aware that:
- Web scraping should be done responsibly
- Respect robots.txt and terms of service
- Adding delays between requests is recommended
- Google may block automated requests