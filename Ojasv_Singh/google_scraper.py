"""
serpapi_search_cli.py
Fetch Google SERP results via SerpAPI (one API key). Outputs CSV + JSON.

Usage:
    python serpapi_search_cli.py --api-key YOUR_KEY --query "Tell me about India" --num 50 --output results

Notes:
 - Provide your SerpAPI key via --api-key or through SERPAPI_API_KEY env var.
 - SerpAPI is a paid service beyond the free trial/quota. Check your account limits.
"""

import argparse
import requests
import time
import csv
import json
import os
from typing import List, Dict

BASE_URL = "https://serpapi.com/search.json"

def parse_args():
    p = argparse.ArgumentParser(description="Fetch Google SERP results using SerpAPI")
    p.add_argument("--api-key", "-k", type=str, default=os.getenv("SERPAPI_API_KEY"),
                   help="SerpAPI API key (or set SERPAPI_API_KEY env var)")
    p.add_argument("--query", "-q", type=str, required=True, help="Search query")
    p.add_argument("--num", "-n", type=int, default=20, help="Total number of organic results to fetch")
    p.add_argument("--output", "-o", type=str, default="serp_results", help="Output filename prefix (without extension)")
    p.add_argument("--gl", type=str, default="us", help="Country of search (gl param, e.g., us, in, uk)")
    p.add_argument("--hl", type=str, default="en", help="Language of search results (hl param)")
    p.add_argument("--google_domain", type=str, default="google.com", help="Google domain to query (google.com, google.co.in, etc.)")
    p.add_argument("--sleep", type=float, default=1.0, help="Seconds to sleep between requests (politeness)")
    p.add_argument("--max-retries", type=int, default=3, help="Retries on transient HTTP errors")
    return p.parse_args()

def serpapi_request(api_key: str, params: Dict, max_retries: int = 3, timeout: int = 15) -> Dict:
    params = params.copy()
    params["api_key"] = api_key
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(BASE_URL, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status and 400 <= status < 500:
                raise
            if attempt < max_retries:
                time.sleep(1.0 * attempt)
                continue
            raise
        except requests.RequestException:
            if attempt < max_retries:
                time.sleep(1.0 * attempt)
                continue
            raise

def extract_results_from_response(resp_json: Dict) -> List[Dict]:
    """
    Extract a list of structured organic results (and any other relevant SERP features).
    This returns a list of dicts with consistent keys.
    """
    rows = []
    organic = resp_json.get("organic_results") or []
    for item in organic:
        row = {
            "position": item.get("position"),
            "title": item.get("title"),
            "link": item.get("link"),
            "displayed_link": item.get("displayed_link"),
            "snippet": item.get("snippet") or item.get("rich_snippet", {}).get("top", {}).get("text"),
            "cached_page": item.get("cached_page"),
            "serpapi_result_id": item.get("result_id"),
            "raw": item
        }
        rows.append(row)
    return rows

def fetch_multiple(api_key: str, query: str, total: int, gl: str, hl: str, google_domain: str,
                   sleep: float = 1.0, max_retries: int = 3) -> List[Dict]:
    collected = []
    fetched = 0
    start = 0 
    per_request = 10  
    while fetched < total:
        to_fetch = min(per_request, total - fetched)
        params = {
            "q": query,
            "engine": "google",
            "num": to_fetch,
            "start": start,       
            "gl": gl,
            "hl": hl,
            "google_domain": google_domain
        }
        resp = serpapi_request(api_key, params, max_retries=max_retries)
        rows = extract_results_from_response(resp)
        if not rows:
            break
        new_rows = []
        existing_links = {r["link"] for r in collected if r.get("link")}
        for r in rows:
            if r.get("link") and r["link"] not in existing_links:
                new_rows.append(r)
                existing_links.add(r["link"])
        if not new_rows:
            break
        collected.extend(new_rows)
        fetched = len(collected)
        start += len(rows)
        time.sleep(sleep)
    return collected[:total]

def save_outputs(rows: List[Dict], prefix: str):
    json_path = f"{prefix}.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(rows, jf, ensure_ascii=False, indent=2)
    csv_path = f"{prefix}.csv"
    fields = ["position", "title", "link", "displayed_link", "snippet", "cached_page"]
    with open(csv_path, "w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: (r.get(k) or "") for k in fields})
    print(f"Saved {len(rows)} items to:\n - {json_path}\n - {csv_path}")

def main():
    args = parse_args()
    if not args.api_key:
        raise SystemExit("Error: SerpAPI API key required (use --api-key or set SERPAPI_API_KEY env var).")
    print(f"Searching for: {args.query!r}  (want {args.num} results)")

    try:
        rows = fetch_multiple(
            api_key=args.api_key,
            query=args.query,
            total=args.num,
            gl=args.gl,
            hl=args.hl,
            google_domain=args.google_domain,
            sleep=args.sleep,
            max_retries=args.max_retries
        )
    except Exception as e:
        raise SystemExit(f"Search failed: {e}")

    if not rows:
        print("No results were fetched. Check your API key, quota, or query parameters.")
        return

    output_rows = []
    for r in rows:
        output_rows.append({
            "position": r.get("position"),
            "title": r.get("title"),
            "link": r.get("link"),
            "displayed_link": r.get("displayed_link"),
            "snippet": r.get("snippet"),
            "cached_page": r.get("cached_page"),
            "raw": r.get("raw")
        })

    save_outputs(output_rows, args.output)

    print("\nTop results:")
    for i, r in enumerate(output_rows[:5], 1):
        print(f"{i}. {r.get('title')}\n   {r.get('link')}\n   {r.get('snippet')}\n")

if __name__ == "__main__":
    main()