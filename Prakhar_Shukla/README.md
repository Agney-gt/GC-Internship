# Google Search Scraper – Selenium Automation

**Author:** Prakhar Shukla  
**Script:** `prakhar_google_scraper.py`  
**Description:** A Python script that uses Selenium to perform Google searches, extract the top search results, and save them into a CSV file. The script supports headless browsing and dynamic CSV filenames.

---

##  Features

- Scrapes **titles, links, and descriptions** from Google search results.  
- Saves results in a **CSV file named after the query** with a timestamp.  
- Supports **headless mode** for automated execution without opening a browser window.  
- Handles **Google consent pop-ups** automatically.  
- Uses **intelligent waits** and scrolling to capture all results.  
- **Auto-installs ChromeDriver** using `webdriver_manager` (no manual driver setup).  

---

##  Requirements

- Python 3.8 or higher  
- Required libraries:
  ```bash
  pip install selenium webdriver-manager
