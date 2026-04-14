from modules.scraping.src.scraper.playwright_webcontent_scraper import PlaywrightWebContentScraper
from modules.scraping.src.scraper.requests_webcontent_scraper import RequestsWebContentScraper


class HybridWebContentScraper:
    def __init__(self, playright_browser=None, playwright_page=None):
        self.requests_scraper = RequestsWebContentScraper()
        self.playwright_scraper = PlaywrightWebContentScraper(browser=playright_browser, page=playwright_page)

    def scrape(self, url):
        try:
            return self.requests_scraper.scrape(url)
        except Exception as requests_exception:
            print(f"Requests scraper failed with error: {requests_exception}")

        try:
            return self.playwright_scraper.scrape(url)
        except Exception as playwright_exception:
            print(f"Playwright scraper failed with error: {playwright_exception}")
            return None