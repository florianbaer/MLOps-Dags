import datetime
from typing import Optional

import pydantic

from modules.scraping.src.crawler.jobs_ch.dto import JobsCHOfferPage


class Location(pydantic.BaseModel):
    street: Optional[str] = None
    region: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: Optional[str] = None


class Company(pydantic.BaseModel):
    name: str
    country: str
    industry: str
    department: str
    location: Optional[Location] = None






class JobChangeEvent(pydantic.BaseModel):
    job: JobsCHOfferPage
    change_date_time: datetime.datetime
    change_type: str
