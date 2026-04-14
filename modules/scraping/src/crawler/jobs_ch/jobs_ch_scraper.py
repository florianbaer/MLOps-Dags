import datetime

from bs4 import BeautifulSoup
from dateutil import parser
from modules.scraping.src.crawler.base_job_scraper import BaseJobScraper
from modules.scraping.src.crawler.jobs_ch.dto import JobsCHOfferPage, JobsOfferingSearchResult
from modules.scraping.src.scraper.webcontent_scraper import WebContentScraper


class JobsCHScraper(BaseJobScraper):
    def __init__(self, webcontent_scraper: WebContentScraper):
        super().__init__(webcontent_scraper=webcontent_scraper)


    def _extract_job(self, job_search_result: JobsOfferingSearchResult, soup: BeautifulSoup) -> JobsCHOfferPage:
        # Title
        title = soup.find('h1', {'data-cy': 'vacancy-title'}).text.strip() if soup.find('h1', {
            'data-cy': 'vacancy-title'}) else None

        # description is content of div with class grid-area_content
        description_html = str(soup.find('div', {'data-cy':"vacancy-description"})) if soup.find('div', {
            'data-cy':"vacancy-description"}) else None
        if description_html is None:
            # find the first div with class grid-area_content
            description_html = str(soup.find('div', {'class': 'grid-area_content'})) if soup.find('div', {
                'class': 'grid-area_content'}) else None

        # Company URL
        company_url_tag = soup.find('a', {'data-cy': 'company-url'})
        company_url = company_url_tag.get('href') if company_url_tag else None

        # Categories
        categories_tags = soup.select('[data-cy="vacancy-meta"] a')
        categories = [tag.text.strip() for tag in categories_tags] if categories_tags else []
        # split categories by / or ,
        categories = [category.strip() for tag in categories for category in tag.split('/')]
        categories = [category.strip() for tag in categories for category in tag.split(',')]

        # Company Rating
        rating_tag = soup.find('span', {'data-cy': 'rating-stars'})
        company_rating = rating_tag.get('title') if rating_tag else None
        try:
            company_rating = company_rating
        except ValueError:
            # if the rating is not available, set it to None
            company_rating = None

        # Company Rating Count
        rating_count_tag = soup.find('span', {'data-cy': 'star-rating-total-reviews'})
        company_rating_count = int(rating_count_tag.text.strip("()")) if rating_count_tag else None

        # Publication Date
        publication_date_tag = soup.find('li', {'data-cy': 'info-publication'})
        publication_date_text = publication_date_tag.find_all('span')[-1].text if publication_date_tag else None
        # auto parse the date
        # try parse

        # Last Updated, Unavailable Since (Placeholder as not present in the sample HTML)
        last_updated = datetime.datetime.now()
        unavailable_since = None

        try:
            publication_date = parser.parse(publication_date_text)
        except:
            publication_date = datetime.datetime.now().timestamp()
            unavailable_since = datetime.datetime.now().timestamp()
            last_updated = datetime.datetime.now().timestamp()

        # Workload
        workload_tag = soup.find('li', {'data-cy': 'info-workload'})
        workload = workload_tag.find_all('span')[-1].text.strip() if workload_tag else None

        # Contract Type
        contract_type_tag = soup.find('li', {'data-cy': 'info-contract'})
        contract_type = contract_type_tag.find_all('span')[-1].text.strip() if contract_type_tag else None

        # Languages
        language_tag = soup.find('li', {'data-cy': 'info-language'})
        language = [language_tag.find_all('span')[-1].text.strip()] if language_tag else None
        if  language is not None and ',' in language[0]:
            language = language[0].split(',')

        # Location (Place of Work)
        location_tag = soup.find('a', {'data-cy': 'info-location-link'})
        location = None

        # check for link
        if location_tag is not None:
            location = location_tag.text.strip() if location_tag else None

        if location is None:
            place_of_work = soup.select('li:-soup-contains("Place of work:")')
            if len(place_of_work) >= 1 and len(place_of_work[0].select('span')) > 2:
                location = place_of_work[0].select('span')[2].text.strip()



        return JobsCHOfferPage(
            title=title,
            job_id=job_search_result.job_id,
            job_url=job_search_result.link,
            company_url=company_url,
            description_html=description_html,
            categories=categories,
            company_rating=company_rating,
            company_rating_count=company_rating_count,
            publication_date=publication_date,
            last_updated=last_updated,
            initial_scrape_date_time=job_search_result.scrape_date_time,
            unavailable_since=unavailable_since,
            workload=workload,
            contract_type=contract_type,
            language=language,
            location=location,
            platform="jobs.ch"
        )