from googleapiclient.discovery import build

import csv

API_KEY = "AIzaSyB2peD7uSAFaQRBtTBOfPu-cBojdXUdWCk"
CSE_ID = "446f331f89a0e4f61"

def scrape_google_api(query, num_results=10):
    service = build("customsearch", "v1", developerKey=API_KEY)
    results = []
    page_limit = (num_results // 10) + 1

    for start in range(1, num_results + 1, 10):
        res = service.cse().list(q=query, cx=CSE_ID, start=start).execute()
        for item in res.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "description": item.get("snippet"),
            })
    return results[:num_results]

def save_to_csv(data, filename="results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link", "description"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} results to {filename}")

if __name__ == "__main__":
    query = input("Enter search query: ")
    results = scrape_google_api(query, 20)
    save_to_csv(results)

    
