from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class SeleniumWebContentScraper(WebContentScraper):
    def __init__(self):
        self.service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.driver = None

    def scrape(self, url):
        # If a driver is provided, check if it is still alive
        if self.driver is None or not self._is_driver_alive(self.driver):
            self.driver = self._get_driver()
        self.driver.get(url)
        text = self._extract_full_text(self.driver.page_source)
        return text

    def _is_driver_alive(self, driver):
        if driver is None:
            return False
        try:
            return driver.service.is_connectable()
        except:
            return False

    def _get_driver(self):
        driver = webdriver.Chrome(options=self.options, service=self.service)
        driver.set_page_load_timeout(10)
        return driver

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()
