# Google Search Scraper

## Overview
A Python-based web scraper using Selenium to extract search results from Google for a given query.

## Features
- Scrape Google search results
- Extract title, link, and snippet for each result
- Save results to CSV
- Headless browser operation
- Advanced anti-bot detection bypass

## Prerequisites
- Python 3.7+
- Chrome browser
- Chrome WebDriver

## Installation
```bash
pip install selenium webdriver-manager
```

## Usage
```bash
python google_scraper.py
```

## Customization
- Modify `search_term` in `main()` to change search query
- Adjust `num_results` to control number of results

## Limitations
- Web scraping may violate Google's Terms of Service
- Results may vary due to dynamic page structure
