from playwright.sync_api import sync_playwright

from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class PlaywrightWebContentScraper(WebContentScraper):
    def __init__(self, browser=None, page=None):
        self.browser = browser
        self.page = page

    def scrape(self, url):
        if not self._is_page_active():
            self._initialize()
        self.page.goto(url)
        content = self.page.content()
        return content

    def _initialize(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.page = self.browser.new_page()

    def _is_page_active(self):
        if self.page is None or self.browser is None:
            return False
        try:
            # Perform a simple operation to check if the page is still accessible
            self.page.title()  # For example, checking the title of the page
            return True
        except Exception as e:
            print(f"Page is not active: {e}")
            return False
