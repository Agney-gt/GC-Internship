import argparse
import json
import os
import time
import uuid
from random import randint

from utils.extract_links_from_webpage import get_links
from utils.request_client import RequestClient
from utils.url_utils import get_filtered_links
import config
from utils.redislite_utils import redis_cleanup, redis_client as redis

request_client = RequestClient()


def write_url_data(url, response_text):
    """Write the response text of the URL to a JSON file."""
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)  # Use os.makedirs for creating directories

    file_path = os.path.join(config.DATA_DIR, f"{uuid.uuid3(uuid.NAMESPACE_URL, str(url))}.json")

    if not os.path.exists(file_path):
        with open(file_path, "w") as fp:
            json.dump({url: response_text}, fp)


class WebsiteScraper:
    def __init__(self, url, start_afresh=False):
        self.url = url
        if start_afresh:
            redis.flushdb()  # Clear the Redis database
        redis.sadd("new_urls", url)  # Add initial URL to the 'new_urls' set in Redis

    def crawl(self, sleep_time_lower=30, sleep_time_upper=121):
        """Crawl the website and process links."""
        print("\nCrawling started...\n")
        write_count = 0
        write_flag = 1

        while redis.smembers("new_urls"):
            url = redis.spop("new_urls")  # Pop a URL from the 'new_urls' set
            redis.sadd("processed_urls", url)  # Mark the URL as processed

            # Sleep logic: random sleep between lower and upper bounds
            time.sleep(randint(sleep_time_lower, sleep_time_upper) if write_count % 12 == 0
                       else randint(sleep_time_lower, sleep_time_upper // 2))

            if write_count % write_flag == 0:
                print(f'Processing {url}')

            write_count += 1

            response = request_client.request_with_proxy_header(url)
            if not response or response.status_code != 200:
                continue  # Skip if no valid response

            # Write the response text to a JSON file
            write_url_data(url, response.text)

            # Get local URLs from the response
            local_urls = list(get_links(response.text, self.url).keys())

            # Filter out foreign URLs or invalid URLs
            local_urls = get_filtered_links(local_urls, self.url)

            # Add new URLs to Redis if they haven't been processed yet
            for new_url in local_urls:
                if not redis.sismember("processed_urls", new_url):
                    redis.sadd("new_urls", new_url)

            # Clean up Redis by removing invalid or processed URLs
            redis_cleanup(self.url)

            if write_count % write_flag == 0:
                print('Processed')

def str2bool(v):
    """Convert a string to a boolean."""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Crawl a website and extract local links.")
    parser.add_argument('website_address', help="The website URL to start crawling.")
    parser.add_argument("-s", "--start_afresh", help="Whether to start fresh (clear Redis).",
                        required=False, default=True, action='store', dest='start_afresh')

    args = parser.parse_args()
    website = args.website_address
    start_afresh = str2bool(args.start_afresh)

    # Validate the website URL
    if not website.startswith("http"):
        print(f"\033[91m Please include website scheme (http/https) in the provided address \033[00m")
        return

    # Start the website scraping process
    scraper = WebsiteScraper(website, start_afresh=start_afresh)
    scraper.crawl(sleep_time_lower=5, sleep_time_upper=18)

if __name__ == '__main__':
    main()
