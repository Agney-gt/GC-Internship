import json
import csv
import pandas as pd
import dicttoxml
import re 

# Function to sanitize the query
def sanitize_query(query, replace_spaces=True, lowercase=True):
    query = re.sub(r'[^a-zA-Z0-9-_ ]', '', query)  # Keep spaces initially
    if replace_spaces:
        query = query.replace(' ', '_')  # Convert spaces to underscores
    if lowercase:
        query = query.lower()
    return query


def save_as_json(results, query):
    filename = f"google_results_{query}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {filename}.")

def save_as_csv(results, query):
    filename = f"google_results_{query}.csv"
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'link', 'description'])
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}.")

def save_as_excel(results, query):
    filename = f"google_results_{query}.xlsx"
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}.")

def save_as_txt(results, query):
    filename = f"google_results_{query}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for idx, result in enumerate(results, 1):
            f.write(f"{idx}. {result['title']}\n")
            f.write(f"Link: {result['link']}\n")
            f.write(f"Description: {result['description']}\n\n")
    print(f"Results saved to {filename}.")

def save_as_xml(results, query):
    filename = f"google_results_{query}.xml"
    xml = dicttoxml.dicttoxml(results, custom_root='search_results', attr_type=False)
    with open(filename, 'wb') as f:
        f.write(xml)
    print(f"Results saved to {filename}.")

def save_as_markdown(results, query):
    filename = f"google_results_{query}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Search Results for: {query}\n\n")
        for idx, result in enumerate(results, 1):
            f.write(f"### {idx}. {result['title']}\n")
            f.write(f"- **Link:** [{result['link']}]({result['link']})\n")
            f.write(f"- **Description:** {result['description']}\n\n")
    print(f"Results saved as Markdown: {filename}")

def save_results(results, query):
    print("\nChoose a format to save results:")
    print("1. JSON\n2. CSV\n3. Excel\n4. TXT\n5. XML\n6. Markdown\n7. Exit without saving")
    choice = input("Enter your choice (1-7): ")

    match choice:  # Requires Python 3.10+
        case '1':
            save_as_json(results, query)
        case '2':
            save_as_csv(results, query)
        case '3':
            save_as_excel(results, query)
        case '4':
            save_as_txt(results, query)
        case '5':
            save_as_xml(results, query)
        case '6':
            save_as_markdown(results, query)
        case '7':
            print("Results were not saved.")
        case _:
            print("Invalid choice. No results were saved.")