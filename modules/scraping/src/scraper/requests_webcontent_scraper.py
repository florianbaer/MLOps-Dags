import requests
from bs4 import BeautifulSoup

from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class RequestsWebContentScraper(WebContentScraper):
    def __init__(self, proxy=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
        }
        self.timeout = 20
        self.proxy = proxy

    def scrape(self, url):
        response = requests.get(url, headers=self.headers, timeout=self.timeout, proxies={"https": self.proxy} if self.proxy is not None else None)
        response.raise_for_status()
        
        return response.text


    def is_200(self, url):
        response = requests.get(url, headers=self.headers, timeout=self.timeout, proxies={"https": self.proxy} if self.proxy is not None else None)

        # check if it was redirected
        if response.history:
            return response.history[0].status_code == 200
        return response.status_code == 200


class ContentExtractionStrategy:
    def extract_content(self, response):
        pass

class FullTextContentExtractionStrategy(ContentExtractionStrategy):
    def extract_content(self, response):
        return BeautifulSoup(response, 'html.parser').get_text(strip=True)

class HtmlContentExtractionStrategy(ContentExtractionStrategy):
    def extract_content(self, response):
        return response.text
