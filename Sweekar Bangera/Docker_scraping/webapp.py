import os
import logging
from flask import Flask, jsonify
from property_scraper import PropertyScraper

app = Flask(__name__)

# Configurability
base_url = os.environ.get('BASE_URL', 'https://proxy.scrapeops.io/v1/')
api_key = os.environ.get('API_KEY', '754f0120-b5e1-4af7-a6f1-8f9ace762f00')
pagination_url = os.environ.get('PAGINATION_URL', 'https://duproprio.com/en/search/list')

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def hello():
    return "Enter '/scrape' in the URL to scape the data"

@app.route('/scrape', methods=['GET'])
def scrape_properties():
    try:
        # Create a scraper instance without specifying the num_pages
        scraper = PropertyScraper(base_url, api_key, pagination_url, num_pages=None)

        # Fetch total number of pages and set it to the scraper instance
        scraper.fetch_total_pages()

        # Check if total pages fetched successfully
        if scraper.num_pages is not None:
            # Now we generate the link for each page after having the updated num_pages and store the page links in a dictionary
            scraper.scrape_pagination_links()

            # Now you can use the scraper to iterate all the links inside the dictionary and fetch the required fields
            property_df = scraper.scrape_property_details()

            # Convert the DataFrame to a JSON response
            property_json = property_df.to_json(orient='records')

            return jsonify({"property_details": property_json})
        else:
            return jsonify({"error": "Failed to fetch total number of pages."})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
