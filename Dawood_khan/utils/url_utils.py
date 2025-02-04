from urllib.parse import urlsplit
from utils.media_extensions import media_extensions_list


def url_split(url):
    """Split the link into useful parts."""
    parts = urlsplit(url)
    scheme = parts.scheme
    base = parts.netloc
    strip_base = base.replace('www.', "")
    base_url = f"{scheme}://{base}"
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return {
        "scheme": scheme,
        "base": base,
        "strip_base": strip_base,
        "base_url": base_url,
        "path": path
    }


def get_filtered_links(local_urls_list, website_full_url):
    """Get the filtered links for a list of local links."""
    filtered_list = []
    strip_base = url_split(website_full_url)["strip_base"].lower()

    for anchor in local_urls_list:
        anchor_lower = anchor.lower()

        # Discard media extensions
        if anchor_lower[anchor_lower.rfind("."):].strip("/") in media_extensions_list:
            continue

        # Discard anchor tags
        if "#" in anchor_lower:
            continue

        # Discard JavaScript tags
        if "javascript:" in anchor_lower:
            continue

        # If the link starts with "http"
        if anchor_lower.startswith("http"):
            http_loc = anchor_lower.find("//")
            end_finder = anchor_lower.find("/", http_loc + 2) if anchor_lower.find("/", http_loc + 2) != -1 else len(anchor_lower)
            if strip_base not in anchor_lower[:end_finder]:
                continue
        else:
            anchor_lower = anchor_lower.strip("/")
            # Discard URLs like "www.google.com/https://www.wikipedia.org"
            end_finder = anchor_lower.find("/") if anchor_lower.find("/") != -1 else len(anchor_lower)
            if strip_base not in anchor_lower[:end_finder]:
                continue

        filtered_list.append(anchor)

    return filtered_list


if __name__ == '__main__':
    pass
