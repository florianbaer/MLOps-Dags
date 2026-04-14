import datetime
from typing import Optional, List, Any
import pydantic
from pydantic_core.core_schema import SerializerFunctionWrapHandler
from google.cloud import firestore


class JobsOfferingSearchResult(pydantic.BaseModel):
    job_id: str
    title: str
    link: str
    platform: str
    scrape_date_time: datetime.datetime

    def __init__(self, job_id: str, title: str, link: str, platform: str):
        super().__init__(job_id=job_id, title=title,  link=link, scrape_date_time=datetime.datetime.now(), platform=platform)


class JobsCHOfferPage(pydantic.BaseModel):
    title: str
    job_id: str
    job_url: str
    description_html: Optional[str] = None
    company_url: Optional[str] = None
    categories: List[str]
    company_rating: Optional[str] = None
    company_rating_count: Optional[int] = None
    publication_date: datetime.datetime
    initial_scrape_date_time: datetime.datetime
    last_updated: datetime.datetime
    unavailable_since: Optional[datetime.datetime] = None
    workload: Optional[str] = None
    contract_type: Optional[str] = None
    language: Optional[List[str]] = None
    location: Optional[str] = None
    platform: str
