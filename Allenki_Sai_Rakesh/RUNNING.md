# Run instructions

## Requirements
- Python 3.9+
- Windows PowerShell (or cmd)
- Internet access

## 1) Open project folder
PowerShell:
```powershell
cd "C:\Users\ALLEN\Downloads\Agney_Nalapat_Onboarding_Task_Optimized"
```

## 2) Create & activate virtual env (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
(cmd.exe: `.venv\Scripts\activate.bat`)

## 3) Install dependencies
```powershell
pip install -r requirements.txt
```
If `requirements.txt` is not present, run:
```powershell
pip install requests beautifulsoup4 pandas
```

## 4) (Optional) Install Playwright fallback
Only if you want the browser fallback for 403 pages:
```powershell
pip install playwright
python -m playwright install
```

## 5) Environment variables (optional)
- Use proxies:
  - set HTTP_PROXY / HTTPS_PROXY in environment if required.
- Force Playwright fallback:
  - PowerShell: `$env:FORCE_PLAYWRIGHT_FALLBACK = "1"`
- Run Playwright headful:
  - PowerShell: `$env:PLAYWRIGHT_HEADFUL = "1"`

## 6) Run the scraper
```powershell
python job_scraper.py
```

## 7) Outputs & logs
- CSV: `job_listings.csv` (in project root)
- Log file: `scraper.log`
- Saved blocked HTML for debugging: `debug_responses/`

## 8) Troubleshooting
- Persistent HTTP 403:
  - Ensure Playwright is installed and try forcing fallback.
  - Add proxies (residential/rotating) if rate-limited.
  - Increase delays or reduce page count in `job_scraper.py`.
- Inspect `debug_responses/blocked_*.html` to see the block page.

## Notes
- Respect the target site's robots.txt and Terms of Service.
- Use scraping responsibly and ethically.