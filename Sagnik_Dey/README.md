# Google Search Scraper

A **robust Selenium-powered scraper** for extracting Google search results — including **titles**, **snippets**, and **URLs** — with support for **headless browsing**, **custom languages**, **auto-saving results**, and **debug mode** for detailed inspection.

This project demonstrates advanced **web automation and DOM handling** using **Selenium WebDriver** and includes **Chrome 142+ headless rendering fixes** for consistent output across environments.

---

## Features

- Extracts **titles**, **snippets**, and **URLs** from Google Search results  
- Supports **custom language codes** (e.g., `en`, `en-IN`, `fr`)  
- Includes **debug mode** for verbose logging and inspection  
- Works flawlessly in both **headless** and **interactive** modes  
- Automatically **saves JSON & CSV results** into a `/results` folder  
- Updated for **Chrome 142+ Headless Rendering Fixes**  
- Automatically handles Google **cookie consent popups**

---

## Project Structure

```markdown
Sagnik_Dey/
│
├── scrape.py             # Main Python script
├── README.md             # Project documentation (this file)
└── results/              # Folder where JSON and CSV outputs are stored
```

---

## Requirements

Before running the scraper, ensure the following:

### Python Environment
- Python 3.9+  
- Recommended: Use a virtual environment

### Dependencies
Install required packages:
```bash
pip install selenium webdriver-manager
```

---

## Browser Requirement

- **Google Chrome** (latest stable version)  
- `chromedriver` is handled automatically by **webdriver-manager**

---

## Usage Examples

### Basic Search
```bash
python scrape.py --query "google swe"
```

### Headless Mode (No GUI)
```bash
python scrape.py --query "bits pilani news" --headless
```

### Custom Language (e.g., Indian English)
```bash
python scrape.py --query "bits pilani news" --lang en-IN
```

### Limit Results & Enable Debug Logs
```bash
python scrape.py --query "bits pilani news" --limit 10 --debug
```

## Command-Line Arguments

| Argument | Description | Default |
|-----------|-------------|----------|
| `--query` / `-q` | Search query | *(required)* |
| `--limit` / `-n` | Number of results to extract | `10` |
| `--headless` | Run Chrome in headless mode | `False` |
| `--lang` | Google interface language (e.g., `en`, `en-IN`, `fr`) | `en` |
| `--debug` | Enable debug mode (extra logs) | `False` |

---

## Automatic Result Saving

All output files are **auto-saved** into a `results/` directory as both `.json` and `.csv`.

### Example:
```markdown
results/
├── bits_pilani_news_results.json
└── bits_pilani_news_results.csv
```

---

## Code Implementation

The following function ensures saving to the results folder automatically:

```python
import os, json, csv

def save_results(results, query):
    os.makedirs("results", exist_ok=True)
    base_name = query.replace(" ", "_")
    json_file = os.path.join("results", f"{base_name}_results.json")
    csv_file = os.path.join("results", f"{base_name}_results.csv")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "snippet", "link"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to 'results/' folder:\n - {json_file}\n - {csv_file}")
```

## Example Output

### Running:
```bash
python scrape.py --query "bits pilani news" --lang en-IN
```

### Produces:
[INFO] Opening: https://www.google.com/search?q=bits+pilani+news&hl=en-IN&pws=0  
[INFO] Extracted 16 results.  
[INFO] Closed browser session.  
Results saved to 'results/' folder:  
results/bits_pilani_news_results.json  
results/bits_pilani_news_results.csv  

---

## Sample JSON Output

```json
[
  {
    "title": "News",
    "snippet": "Stay informed with the latest happenings at BITS Pilani...",
    "link": "https://www.bits-pilani.ac.in/news/"
  },
  {
    "title": "bits pilani news",
    "snippet": "BITS Pilani introduces new UG and PG courses...",
    "link": "https://indianexpress.com/about/bits-pilani/"
  }
]
```

## Implementation Notes

- Uses **Selenium WebDriver** for browser automation  
- Employs **explicit waits (`WebDriverWait`)** to ensure DOM elements load fully  
- Includes **scroll-based lazy loading** for dynamically loaded results  
- **Automatically accepts cookie pop-ups** when encountered  
- Detects and adapts to multiple Google layout structures:
  - `div.tF2Cxc`
  - `div.MjjYud`
  - `div.g`