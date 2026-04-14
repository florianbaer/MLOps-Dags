from bs4 import BeautifulSoup


class WebContentScraper:
    def scrape(self, url):
        pass

    def check_status_code(self, response):
        pass

    def _extract_full_text(self, html):
        return BeautifulSoup(html, 'html.parser').get_text(strip=True)