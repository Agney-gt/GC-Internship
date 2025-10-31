#Overview
This Python tool uses Selenium to search Google. It automatically grabs the Title, Link, and Description from search results and saves them to a clean CSV file.

#How It Works
-The script opens Chrome automatically.
-It searches Google using your entered topic.
-It collects the top result titles, links, and descriptions.
-It saves everything to a CSV file named after your search query (e.g., google_results_your_topic.csv).

#Setup
1.Requirements:
-Python
-Chrome
2.Installation:
Run this simple command:
pip install selenium webdriver-manager