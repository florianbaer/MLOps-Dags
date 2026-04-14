from typing import Tuple

from modules.scraping.src.crawler.base_job_scraper import BaseJobScraper
from modules.scraping.src.crawler.base_job_searcher import BaseJobSearcher
from modules.scraping.src.crawler.jobs_ch.jobs_ch_scraper import JobsCHScraper
from modules.scraping.src.crawler.jobs_ch.jobs_ch_searcher import JobsCHSearcher
from modules.scraping.src.scraper.requests_webcontent_scraper import RequestsWebContentScraper


class CrawlerFactory:
    def __init__(self):
        self.implented_platforms = ['jobs.ch']

    def get_crawler(self, platform) -> Tuple[BaseJobSearcher, BaseJobScraper]:
        if platform not in self.implented_platforms:
            raise ValueError('Platform not implemented, available platforms are: ' + ', '.join(self.implented_platforms))

        if platform == 'jobs.ch':
            requests_webcontentscraper = RequestsWebContentScraper()
            return JobsCHSearcher(webcontent_scraper=requests_webcontentscraper), JobsCHScraper(webcontent_scraper=requests_webcontentscraper)
        else:
            raise ValueError('Unknown platform')

    def available_platforms(self):
        return self.implented_platforms
