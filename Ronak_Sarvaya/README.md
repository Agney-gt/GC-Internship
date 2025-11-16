# Google Search Scraper - Ronak Sarvaya

A robust Selenium-based web scraper for extracting Google search results.

## Features

- ✅ Modern Selenium 4+ implementation
- ✅ Automatic ChromeDriver management (no manual driver download needed)
- ✅ Extracts title, URL, and snippet for each result
- ✅ Saves results to CSV file with timestamp
- ✅ Configurable headless/visible browser mode
- ✅ Proper error handling and explicit waits
- ✅ Anti-detection measures (user-agent, automation flags)

## Installation

### Prerequisites
- Python 3.7 or higher
- Google Chrome browser installed

### Install Required Packages

```bash
pip install selenium webdriver-manager
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python my_scraper.py
```

### Customize Search Query

Edit the `main()` function in `my_scraper.py`:

```python
# Configuration
SEARCH_QUERY = "Your search query here"  # Change this
NUM_RESULTS = 10                          # Number of results to scrape
HEADLESS_MODE = True                      # False to see browser window
```

### Use as a Module

```python
from my_scraper import GoogleScraper

# Create scraper instance
scraper = GoogleScraper(headless=True)

# Scrape Google
results = scraper.scrape(
    query="Python tutorials",
    num_results=15,
    save_csv=True
)

# Access results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['snippet']}")
```

## Output

The scraper generates a CSV file with the following columns:
- **rank**: Position in search results (1-based)
- **title**: Page title
- **url**: Page URL
- **snippet**: Description/snippet from search results

Output filename format: `google_results_YYYYMMDD_HHMMSS.csv`

## Configuration Options

### GoogleScraper Class

```python
scraper = GoogleScraper(headless=True)
```

- `headless` (bool): Run browser in headless mode (default: True)

### scrape() Method

```python
results = scraper.scrape(query, num_results=10, save_csv=True)
```

- `query` (str): Search query string
- `num_results` (int): Maximum number of results to extract (default: 10)
- `save_csv` (bool): Save results to CSV file (default: True)

## Troubleshooting

### ChromeDriver Issues
The scraper uses `webdriver-manager` to automatically download and manage ChromeDriver. If you encounter issues:

```bash
pip install --upgrade webdriver-manager
```

### Import Errors
Make sure all dependencies are installed:

```bash
pip install selenium webdriver-manager
```

### No Results Found
- Check your internet connection
- Try running in non-headless mode to see what's happening
- Google may be blocking automated requests - try adding delays

## Example Output

```
============================================================
Google Search Scraper - Ronak Sarvaya
============================================================
✅ Chrome WebDriver initialized successfully
🔍 Searching Google for: 'Python programming tutorials'
✅ Search completed successfully
📊 Found 10 search results
✓ Extracted result #1: Python Tutorial - W3Schools...
✓ Extracted result #2: Learn Python Programming...
...
✅ Successfully extracted 10 results
✅ Results saved to: Ronak_Sarvaya/google_results_20240115_143022.csv
✅ Browser closed

============================================================
SEARCH RESULTS
============================================================

[1] Python Tutorial - W3Schools
URL: https://www.w3schools.com/python/
Snippet: Well organized and easy to understand Web building tutorials...
------------------------------------------------------------
...
```

## Notes

- Respect Google's Terms of Service
- Use reasonable delays between requests
- Consider using Google's official APIs for production use
- This scraper is for educational purposes

## Author

**Ronak Sarvaya**  
GC-Internship Project
