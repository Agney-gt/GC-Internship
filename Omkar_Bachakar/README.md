# 🔍 Google Search Automation using Selenium

This project automates Google Search using **Python** and **Selenium WebDriver**.  
It opens Google in Chrome, performs a search for your chosen query, and extracts the **title**, **link**, and **snippet** from the top search results.

---

## 🚀 Features

- Automates the Google search process.
- Extracts titles, links, and short snippets from search results.
- Uses Selenium WebDriver for browser automation.
- Automatically closes the browser after execution.

---

## 🧠 Tech Stack

- **Python 3.x**
- **Selenium**
- **Chrome WebDriver**

---

## ⚙️ Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/<your-username>/google-search-automation-using-selenium.git
   cd google-search-automation-using-selenium
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up ChromeDriver:**
   - Download it from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
   - Make sure it matches your Chrome version.
   - Add it to your system PATH.

---

## ▶️ Usage

1. Open the file `google_search.py`.
2. Change the search query:
   ```python
   search_query = "Python tutorials"
   ```
3. Run the script:
   ```bash
   python google_search.py
   ```
4. You’ll see the search results printed in your terminal:
   ```
   Result 1:
   Title: Learn Python - W3Schools
   Link: https://www.w3schools.com/python/
   Snippet: Learn Python with examples and exercises...
   ```

---

## 📂 Project Structure

```
google-search-automation-using-selenium/
│
├── google_search.py      # Main Python script
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

---

## 💡 Example Use Cases

- Automating keyword research.
- Scraping data for SEO analysis.
- Learning Selenium automation.
- Practicing Python web scraping.

---

## 🧑‍💻 Author

**Omkar Bachakar**  
A passionate learner exploring Python, automation, and web development.

---

## 🪪 License

This project is open source and available under the [MIT License](LICENSE).
