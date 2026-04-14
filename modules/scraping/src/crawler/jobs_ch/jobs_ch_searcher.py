import os
from http.client import responses
from typing import List, Dict, Any
from urllib.parse import urlparse, unquote

from modules.scraping.src.crawler.base_job_searcher import BaseJobSearcher, BaseJobsSearchResult
from modules.scraping.src.crawler.jobs_ch.dto import JobsOfferingSearchResult
from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class JobsCHSearchResult(BaseJobsSearchResult):
    def __init__(self, query_dict: Dict[str, str], jobs: List[JobsOfferingSearchResult], page_key: str = "page"):
        super().__init__(query_dict, jobs, page_key)



class JobsCHSearcher(BaseJobSearcher):
    def __init__(self, webcontent_scraper: WebContentScraper):
        super().__init__(webcontent_scraper=webcontent_scraper, base_search_url= "https://www.jobs.ch/en/vacancies/?", required_arguments=[], valid_arguments=["term", "location", "page", 'region'], page_key="page")
        self.existing_job_ids= None

    def set_existing_job_ids(self, existing_job_ids: List[str]):
        self.existing_job_ids = existing_job_ids

    def search(self, query_dict: Dict[str, Any]) -> JobsCHSearchResult:
        return self._search(query_dict)

    def _extract_last_path_segment(self, url:str):
        """
        Extracts the last segment of a URL path using os.path.basename
        for structured path handling.
        """
        parsed_url = urlparse(url)
        return unquote(os.path.basename(parsed_url.path.rstrip('/')))

    def _extract_search_results(self, soup) -> List[JobsOfferingSearchResult]:

        jobs = []
        for article in soup.find_all("article", {"data-cy": "serp-item"}):
            title = article.find("a", {"data-cy": "job-link"}).get("title", "").strip()
            link = article.find("a", {"data-cy": "job-link"}).get("href", "").strip()
            link = "https://www.jobs.ch" + link
            job_id = self._extract_last_path_segment(link)

            if self.existing_job_ids is not None and job_id in self.existing_job_ids:
                continue

            jobs.append(JobsOfferingSearchResult(job_id=job_id, title=title, link=link, platform="jobs.ch"))
            self.existing_job_ids.append(job_id)

        return jobs
