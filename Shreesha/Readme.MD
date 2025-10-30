#Google search Scraper

#Overview
This Python project uses Selenium to automatically search on Google and collect the title, description, and link from the search results.  
Each time you run it, a new CSV file is created with the current date and time.

#What it does
- Opens Google and searches for what you type  
- Gets the top search results  
- Saves the results (Title, Description, Link) in a CSV file  
- Creates a new file every time (example:  
  `google_results_python_20251030_223045.csv`)

#Requirements
- Python 3  
- Google Chrome  
- ChromeDriver  
- selenium
