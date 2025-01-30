# Google Search Scraper using Selenium

This script automates Google search using **Selenium** and **ChromeDriver**, extracts the top 10 search results, and saves them in a CSV file.

## Features
- Takes **user input** for the search term and output file name.
- Uses **Selenium with Chrome WebDriver** for automation.
- Extracts **top 10 search results** (titles and URLs).
- Saves results to a CSV file.

## Requirements
Make sure you have the following installed before running the script:
- Python 3.
- Google Chrome
- ChromeDriver (matching your Chrome version)
- Selenium library (install using `pip`):
  ```bash
  pip install selenium
  ```

## Setup
1. Download and install **ChromeDriver** from [here](https://chromedriver.chromium.org/downloads).  
2. Ensure **ChromeDriver** is accessible in your system's PATH.
3. Run the script:
   ```bash
   python google_scraper.py
   ```

## How It Works
1. The script prompts you for a **search term** and a **file name**.
2. It performs a **Google search** using Selenium.
3. Extracts the **top 10 results** (title + link).
4. Saves them in the specified **CSV file**.

## Example Usage
```
Enter search term: Python programming
Enter file name (without .csv): python_results
```
This will generate a file named `python_results.csv` containing the results.

## Output Format
The CSV file will have two columns:

| Title | Link |
|-------|------|
| Python Tutorial - W3Schools | https://www.w3schools.com/python/ |
| Learn Python - Python.org | https://www.python.org/ |

## Notes
- If the script isn't working, ensure **ChromeDriver** is up-to-date.
- Google may occasionally change its page structure, requiring updates to the script.

---

This was a quick project to get familiar with Selenium and web scraping. Feel free to modify and improve it!
