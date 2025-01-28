# Google Search Automation

This project automates Google searches and stores the results in multiple formats such as JSON, CSV, Excel, TXT, XML, and Markdown.

## Features
- Automates Google search for user-provided queries.
- Collects titles, links, and descriptions of search results.
- Allows the user to choose the number of results to display.
- Offers options to save results in different file formats.
- Prevents duplicate results by tracking visited links.

## Requirements
- Python 3.7+
- Selenium
- WebDriver-Manager
- Pandas
- dicttoxml

## Setup

1. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

2. Run the script
    ```bash
    python search_automation.py
    ```

    - Enter the search query and choose how many results you want.
    - Choose the file format to save the results (JSON, CSV, Excel, etc.).

## Files
- `search_automation.py`: Main script to run the search and collect results.
- `save_results.py`: Handles saving results to various formats.
- `requirements.txt`: Python dependencies.