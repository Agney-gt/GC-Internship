# Google Search Scraper using Selenium

A simple and efficient Python script that uses Selenium WebDriver with XPath selectors to scrape Google search results.

## 🌟 Features

- ✅ **XPath-only selectors** - Uses only XPath for element location
- ✅ **Anti-detection measures** - Bypasses bot detection with custom configurations
- ✅ **Smart result filtering** - Automatically skips empty/invalid results
- ✅ **Browser stays open** - View results in Chrome as long as you need
- ✅ **Clean terminal output** - Displays results with rank, title, and URL
- ✅ **Error handling** - Robust exception handling for stable scraping

## 📋 Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (automatically managed by Selenium 4.6+)

## 🚀 Installation

1. **Install Selenium:**

```bash
pip install selenium
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

Run the script:

```bash
python google_scraper.py
```

Follow the prompts:
1. **Enter search query**: Type what you want to search for
2. **Enter number of results**: Specify how many results (default: 10)
3. **View results**: Results appear both in browser and terminal
4. **Exit**: Press `Ctrl+C` to close the browser and exit

### Example

```
Search query: Python programming
Number of results (10): 10

Opening Google...
Searching...
Extracting results...
1. Welcome to Python.org
2. Python Tutorial - W3Schools
3. Learn Python - Free Interactive Python Tutorial
...
10. Python Programming Language

✓ Scraped 10 results
Browser will remain open. Press Ctrl+C in terminal to exit.

======================================================================
1. Welcome to Python.org
   https://www.python.org/

2. Python Tutorial - W3Schools
   https://www.w3schools.com/python/
...
======================================================================
```

## 🔧 How It Works

### 1. **Anti-Detection Setup**
```python
- Custom user agent
- Disabled automation flags
- CDP command for user agent override
- Webdriver property masking
```

### 2. **XPath-Based Scraping**
The script uses XPath expressions to locate elements:
- Search box: `//textarea[@name='q']` or `//input[@name='q']`
- Results container: `(//div[contains(@class, 'g') and .//h3])[i]`
- Title: `//h3`
- URL: `//a[@href]`
- Description: `//div[contains(@class, 'VwiC3b')]`

### 3. **Smart Result Collection**
- Skips empty or invalid results
- Continues searching until requested number of valid results found
- Maximum 20 extra attempts to avoid infinite loops

## 📊 Output Format

Results are displayed in terminal with:
- **Rank**: Position number (1, 2, 3, ...)
- **Title**: Page title from search result
- **URL**: Full webpage URL
- **Description**: Snippet from Google (if available)

## ⚙️ Configuration

### Headless Mode
To run without opening a visible browser:
```python
results = scrape_google(query, num_results, headless=True)
```

### Custom Number of Results
Default is 10, but you can specify any number:
```python
results = scrape_google("your query", 20)  # Get 20 results
```

## 🛠️ Code Structure

```
google_scraper.py
├── setup_driver()        # Configures Chrome with anti-detection
├── scrape_google()       # Main scraping function
└── main()                # User interface and result display
```

## ⚠️ Important Notes

### Browser Behavior
- Browser **stays open** after scraping completes
- Press `Ctrl+C` in terminal to close browser and exit
- Script keeps running in an infinite loop to maintain browser session

### Rate Limiting
- Built-in delays (3-5 seconds) between actions
- Respectful of Google's servers
- Avoid running too frequently

### Legal & Ethical Use
- ⚠️ **Respect Google's Terms of Service**
- 🚫 Don't use for automated/commercial scraping at scale
- ✅ Use responsibly for educational/personal purposes only
- ⚠️ Consider Google's robots.txt policies

## 🐛 Troubleshooting

### ChromeDriver Issues
```bash
pip install --upgrade selenium
```
Selenium 4.6+ manages ChromeDriver automatically.

### Empty Results
- Some results may be ads or special content
- Script automatically skips these and continues
- Searches up to 20 extra results to find valid ones

### Browser Closes Immediately
- Make sure you don't have errors in terminal
- The infinite loop should keep browser open
- Check that Selenium is properly installed

### Import Errors
```bash
pip install selenium
```

## 📝 Requirements

```
selenium>=4.6.0
```

## 🎯 Best Practices

1. **Don't scrape too frequently** - Add delays between runs
2. **Respect robots.txt** - Check Google's crawling policies
3. **Use for learning** - Great for understanding web scraping
4. **Be ethical** - Don't overwhelm servers with requests

## 📄 License

This project is for educational purposes only.

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements.

---

**Note**: Web scraping should always be done responsibly and in compliance with the website's terms of service and applicable laws.
