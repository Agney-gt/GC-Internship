# Google Search Scraper using Selenium

A Python script that uses Selenium WebDriver to scrape Google search results.

## Features

- ✅ Scrapes Google search results (title, URL, description)
- ✅ Configurable number of results to scrape
- ✅ Headless mode option for background execution
- ✅ Export results to CSV or JSON format
- ✅ Anti-detection measures to avoid being blocked
- ✅ User-friendly command-line interface

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (automatically managed by Selenium 4.6+)

## Installation

1. **Install required packages:**

```bash
pip install selenium
```

Or install all dependencies from requirements.txt (if available):

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script:

```bash
python google_scraper.py
```

The script will prompt you for:
- Search query
- Number of results to scrape
- Export format (CSV/JSON/none)

### Using as a Module

You can also import and use the scraper in your own code:

```python
from google_scraper import GoogleScraper

# Create scraper instance
scraper = GoogleScraper(headless=True)

# Search and get results
results = scraper.search_google("Python programming", num_results=10)

# Save results
scraper.save_to_csv("my_results.csv")
scraper.save_to_json("my_results.json")

# Close the browser
scraper.close()
```

### Advanced Usage

```python
from google_scraper import GoogleScraper

# Initialize with headless mode
scraper = GoogleScraper(headless=True)

try:
    # Perform search
    results = scraper.search_google("machine learning tutorials", num_results=20)
    
    # Process results
    for result in results:
        print(f"{result['rank']}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Description: {result['description']}\n")
    
    # Save to both formats
    scraper.save_to_csv("ml_tutorials.csv")
    scraper.save_to_json("ml_tutorials.json")
    
finally:
    scraper.close()
```

## Output Format

### CSV Format
The CSV file contains the following columns:
- `rank`: Position in search results (1, 2, 3, ...)
- `title`: Title of the search result
- `url`: URL of the webpage
- `description`: Snippet/description from Google

### JSON Format
```json
[
    {
        "rank": 1,
        "title": "Example Title",
        "url": "https://example.com",
        "description": "Example description text..."
    },
    ...
]
```

## Configuration Options

### Headless Mode
Run the browser in the background without GUI:
```python
scraper = GoogleScraper(headless=True)
```

### Number of Results
Specify how many results to scrape:
```python
results = scraper.search_google("query", num_results=20)
```

## Features Explained

### Anti-Detection Measures
The scraper includes several techniques to avoid being detected as a bot:
- Custom user agent
- Disabled automation flags
- Randomized delays
- WebDriver property masking

### Error Handling
The script includes robust error handling for:
- Network issues
- Element not found errors
- Browser crashes
- Invalid queries

## Troubleshooting

### ChromeDriver Issues
If you get ChromeDriver errors:
```bash
pip install --upgrade selenium
```

Selenium 4.6+ automatically manages ChromeDriver.

### Import Errors
If you see "ModuleNotFoundError: No module named 'selenium'":
```bash
pip install selenium
```

### Google Blocking
If Google blocks your requests:
- Add delays between searches
- Use headless mode sparingly
- Don't scrape too frequently
- Consider using proxies for large-scale scraping

## Notes

- **Respect Google's Terms of Service**: Use this tool responsibly
- **Rate Limiting**: Don't send too many requests in a short time
- **Legal Considerations**: Ensure your use case complies with applicable laws
- **Robots.txt**: Be aware of Google's robots.txt file

## Example Output

```
Searching for: Python programming
Chrome WebDriver started successfully.
Result 1: Welcome to Python.org
Result 2: Python Tutorial - W3Schools
Result 3: Learn Python - Free Interactive Python Tutorial
...
Successfully scraped 10 results.

Results saved to google_search_results.csv
WebDriver closed.
```

## License

This project is for educational purposes only.

## Contributing

Feel free to submit issues or pull requests for improvements.
