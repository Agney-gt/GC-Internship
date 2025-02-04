from redislite import Redis
from utils.url_utils import get_filtered_links


# Initialize Redis client with automatic decoding of responses
redis_client = Redis(dbfilename="./redis.db", decode_responses=True)


def redis_cleanup(website_full_url):
    """Removes invalid entries from Redis caches"""
    try:
        # Remove intersections (already processed URLs) from "new_urls"
        new_urls = redis_client.smembers("new_urls")
        processed_urls = redis_client.smembers("processed_urls")

        # Remove processed URLs from "new_urls" set
        for anchor in redis_client.sinter("new_urls", "processed_urls"):
            redis_client.srem("new_urls", anchor)
            print(f"Removed processed URL from redis: {anchor}!\n")

        # Check all remaining URLs in "new_urls" for validity
        for anchor in new_urls:
            # Filter the links based on some criteria from the utility function
            if len(get_filtered_links([anchor], website_full_url)) < 1:
                redis_client.srem("new_urls", anchor)
                print(f"Removed invalid URL from redis: {anchor}!\n")

    except Exception as e:
        print(f"Error during Redis cleanup: {e}")


if __name__ == '__main__':
    # Call the cleanup function for the given website URL
    redis_cleanup("https://www.wikipedia.org/")
