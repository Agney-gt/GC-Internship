from requests.auth import HTTPProxyAuth
from utils.proxy_utils.proxy import Proxy, ua
import requests
import config


class RequestClient(Proxy):
    def __init__(self):
        super().__init__()

    def request_with_proxy_header(self, url):
        """
        Make a request to the given URL using a proxy if enabled, and with a User-Agent header.
        """
        header = {'User-Agent': ua.user_agent()}

        if config.USE_PROXY_SERVER:
            proxy = self.generate_proxy()
            auth = HTTPProxyAuth("", "")
            try:
                # Attempt request with proxy
                response = requests.get(url, proxies=proxy, auth=auth, headers=header, timeout=20, verify=True)
                return response
            except requests.RequestException as e:
                # Log error and remove invalid proxy from list
                print(f"Error with proxy {proxy.get('http')}: {e}")
                self.proxy_list.remove(proxy.get("http"))
                self.write_proxy_list()
                return None
        else:
            try:
                # Attempt request without proxy
                response = requests.get(url, headers=header, timeout=20, verify=True)
                return response
            except requests.RequestException as e:
                # Log error if the request fails without a proxy
                print(f"Error without proxy: {e}")
                return None


if __name__ == '__main__':
    cli = RequestClient()
    response = cli.request_with_proxy_header("https://www.wikipedia.org/")
    if response:
        print(response.text)
    else:
        print("Failed to retrieve the webpage.")
