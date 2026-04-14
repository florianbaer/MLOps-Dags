import abc
import urllib
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from modules.scraping.src.crawler.jobs_ch.dto import JobsOfferingSearchResult
from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class BaseJobsSearchResult(abc.ABC):
    def __init__(self, query_dict: Dict[str, str], jobs: List[JobsOfferingSearchResult], page_key: str = "page"):
        self.found_jobs: List[JobsOfferingSearchResult] = jobs
        self.page = 1
        self.query_dict = query_dict
        self.page_key = page_key

    def get_next_page_arguments(self) -> Dict[str, str]:
        self.page += 1
        self.query_dict[self.page_key] = str(self.page)
        return self


class BaseJobSearcher(abc.ABC):
    def __init__(self, webcontent_scraper: WebContentScraper, base_search_url: str, required_arguments: List[str],
                 valid_arguments: List[str], page_key: Optional[str] = None):
        self.BASE_SEARCH_URL = base_search_url
        self.required_arguments = required_arguments
        self.valid_arguments = valid_arguments
        self.webcontent_scraper = webcontent_scraper
        self.page_key = page_key
        self.query_dict = None



    @abc.abstractmethod
    def search(self, query_dict: Dict[str, Any]) -> BaseJobsSearchResult:
        pass

    def next_page(self) -> BaseJobsSearchResult:
        if self.query_dict is None:
            raise ValueError("No query has been executed yet")
        if self.page_key is None:
            raise ValueError("No page key has been set, paging is not supported")
        self.query_dict[self.page_key] = str(int(self.query_dict[self.page_key]) + 1)
        return self._search(self.query_dict)

    def does_next_page_exist(self) -> bool:
        url = self.BASE_SEARCH_URL + self.get_query_string(self.query_dict)
        return self.webcontent_scraper.is_200(url)

    def _search(self, query_dict: Dict[str, Any]) -> BaseJobsSearchResult:
        self.query_dict = query_dict
        url = self.BASE_SEARCH_URL + self.get_query_string(self.query_dict)
        response = self.webcontent_scraper.scrape(url)
        soup = self._get_soup(response)
        jobs = self._extract_search_results(soup)
        return BaseJobsSearchResult(query_dict, jobs)

    def _get_soup(self, response):
        return BeautifulSoup(response, 'html.parser')

    def get_query_string(self, arguments: dict) -> str:
        arguments = self._filter_arguments(arguments)

        # if any of the arguments contain a list, convert to a list of Tuple[str, str] with duplicate keys
        for key, value in arguments.items():
            if isinstance(value, list):
                arguments[key] = [(key, str(val)) for val in value]

        return urlencode(arguments)

    def _filter_arguments(self, arguments: dict):
        if not all(arg in arguments for arg in self.required_arguments):
            raise ValueError(f"Arguments must contain the following keys: {', '.join(self.required_arguments)}")
        return {key: value for key, value in arguments.items() if key in self.valid_arguments}

    @abc.abstractmethod
    def _extract_search_results(self, soup: BeautifulSoup) -> List[JobsOfferingSearchResult]:
        pass
