import logging
import urllib.parse
import requests


class TinyURLShortener:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.URL = "https://tinyurl.com/api-create.php"

    def shorten(self, url_long):
        try:
            url = self.URL + "?" + urllib.parse.urlencode({"url": url_long})
            res = requests.get(url)
            if res.status_code == 200:
                return res.text
            else:
                raise Exception(f"Failed to shorten URL. Status code: {res.status_code}")
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Request failed: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


tiny_url = TinyURLShortener().shorten
