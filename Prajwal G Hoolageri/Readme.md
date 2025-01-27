# Google Scraper with CAPTCHA Handling

This script allows you to scrape Google search results using Selenium while bypassing Google’s automation detection mechanisms. The scraped results are saved in a JSON file and displayed in the console.

## Features
- **Stealth Mode:** Uses `selenium-stealth` to bypass bot detection.
- **CAPTCHA Handling:** Waits for manual CAPTCHA resolution and proceeds once search results are loaded.
- **Search Results:** Extracts titles, URLs, and descriptions of the search results.
- **Save to JSON:** Saves the scraped data in a structured JSON file.

## Prerequisites
1. Python 3.x installed.
2. Install required Python packages:
   ```bash
   pip install selenium webdriver-manager selenium-stealth
   ```
3. Google Chrome installed on your system.

## How to Use
1. Clone or download the script.
2. Run the script in your terminal or IDE:
   ```bash
   python google_scraper.py
   ```
3. Enter your search query when prompted.
4. Solve the CAPTCHA manually if it appears.
5. The script will scrape the results and save them to a JSON file named `google_results.json`.

## Script Breakdown
- **Selenium WebDriver Setup:** Configured to mimic a real user by using stealth mode.
- **Search Query Execution:** Automates entering the query and navigating the search results page.
- **CAPTCHA Handling:** Instructs the user to solve the CAPTCHA and waits until the results are loaded.
- **Result Extraction:** Extracts the title, URL, and description of each search result.
- **Save Results:** Saves the data into a JSON file for easy reuse.

## Example Output
A sample JSON output file, `google_results.json`, will look like this:
```json
[
    {
        "Title": "Example Title 1",
        "Link": "https://example.com",
        "Description": "This is an example description."
    },
    {
        "Title": "Example Title 2",
        "Link": "https://example2.com",
        "Description": "Another example description."
    }
]
```