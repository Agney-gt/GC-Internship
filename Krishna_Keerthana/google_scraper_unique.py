import pandas as pd
from serpapi import GoogleSearch
import os

api_key = "701ca4ff846fe1633c9fc764638b9c9269fe21c0f910389f39929b80ae66efc2"

query = "AI projects for students"

params = {
    "engine": "google",
    "q": query,
    "api_key": api_key,
    "num": 20
}

search = GoogleSearch(params)
results = search.get_dict()

if "organic_results" in results:
    data = []
    for item in results["organic_results"]:
        title = item.get("title", "N/A")
        link = item.get("link", "N/A")
        snippet = item.get("snippet", "N/A")
        data.append({"Title": title, "Link": link, "Snippet": snippet})

    output_file = "Keerthana_google_results.csv"
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8")

    abs_path = os.path.abspath(output_file)
    print(f"✅ Results saved successfully!")
    print(f"📁 File Location: {abs_path}")

else:
    print("⚠️ No search results found. Check your query or API key.")
