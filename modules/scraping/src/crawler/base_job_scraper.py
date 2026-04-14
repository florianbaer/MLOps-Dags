import abc
from http.client import responses

from bs4 import BeautifulSoup

from modules.scraping.src.crawler.base_job_searcher import BaseJobsSearchResult
from modules.scraping.src.crawler.jobs_ch.dto import JobsOfferingSearchResult
from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper
from modules.scraping.src.utils.logger import get_logger


class BaseJobScraper:
    def __init__(self, webcontent_scraper: WebContentScraper):
        self.webcontent_scraper = webcontent_scraper
        self.logger = get_logger(__name__)

    def _get_soup(self, response):
        return BeautifulSoup(response, 'html.parser')

    def _crawl(self, url: str) -> BaseJobsSearchResult:
        try :
            response = self.webcontent_scraper.scrape(url)
        except Exception as e:
            self.logger.error(f"Failed to scrape {url} with error: {e}")
            return None
        return self._get_soup(response)

    @abc.abstractmethod
    def _extract_job(self, job_search_result: JobsOfferingSearchResult, soup: BeautifulSoup):
        pass

    def run(self, job: JobsOfferingSearchResult):
        soup = self._crawl(job.link)
        try:
            job = self._extract_job(job_search_result=job, soup=soup)
            return job
        except Exception as e:
            self.logger.error(f"Failed to extract job from {job.link} with error: {e}")
            # print stack trace
            import traceback
            traceback.print_exc()
            return None


