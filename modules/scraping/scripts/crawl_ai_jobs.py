from modules.scraping.src.data.jobs.firestore import AsyncFirestoreService
from modules.scraping.src.search_term.search_term_generator import SimpleSearchQueryGenerator
from modules.scraping.src.utils.logger import get_logger
import pyfiglet
import asyncio
import random

from modules.scraping.src.crawler.crawler_factory import CrawlerFactory


class Program():
    def __init__(self):
        self.logger = get_logger(__name__)
        project_name = "sage-mind-371111"
        collection_name = 'swiss-ai-jobs'
        database_name = 'swiss-ai-jobs'
        self.service = AsyncFirestoreService(project_name=project_name, collection_name=collection_name,
                                             database_name=database_name)

        self.title()
        self.logger.debug('Starting AI JOBS Monitor Crawler')

    def title(self):
        f = pyfiglet.Figlet(font='small')
        print(f.renderText('DEMO Crawler'))

    async def crawl_jobs(self, crawler, response):

        for job in response.found_jobs:
            try:
                job_page = crawler.run(job)
                self.logger.info(f'Job crawled: {job.job_id} - {job.link}')
                await self.service.create(job_page.job_id, job_page.model_dump())
            except Exception as e:
                self.logger.error(f'Error while crawling job: {job.job_id} - {str(e)}, {job.link}')
                # print stack trace here
                import traceback
                traceback.print_exc()

    async def main(self):

        factory = CrawlerFactory()

        for platform in factory.available_platforms():
            for term, region in self._get_search_term_generator().generate_search_query():

                self.logger.debug(f'Crawling jobs from: {platform}')
                searcher, crawler = factory.get_crawler(platform)

                document_ids = await self.service.get_existing_ids()

                searcher.set_existing_job_ids(document_ids)

                response = searcher.search({"term": term, 'region': region, "page": 1})

                next_page_exists = True

                while next_page_exists:
                    self.logger.info(f'Crawling page {searcher.query_dict[searcher.page_key]} for term: {term}')
                    await self.crawl_jobs(crawler, response)
                    next_page_exists = searcher.does_next_page_exist()
                    if not next_page_exists:
                        break
                    response = searcher.next_page()

    def _get_search_term_generator(self):
        search_terms = ['Optimization', 'Robotics', 'Machine Learning', 'Deep Learning', 'Computer Vision',
                        'Natural Language Processing', 'NLP', 'Data Science', 'Artificial Intelligence',
                        'Data Engineering', 'Data Analyst', 'Software Engineer', 'Computer Science', 'Data Mining',
                        'Big Data', 'Data Analytics', 'Data Visualization', 'Business Intelligence', 'Data Warehousing',
                        'Data Integration', 'Data Quality', 'Data Governance', 'Data Security', 'Data Privacy',
                        ]

        # shuffle search terms
        random.shuffle(search_terms)
        search_terms = search_terms[:5]

        search_terms = set(search_terms)

        search_terms = list(search_terms)

        locations = [7, 12, 15, 2, 3, 4, 5]
        return SimpleSearchQueryGenerator(search_terms, locations)


if __name__ == '__main__':
    program = Program()

    asyncio.run(program.main())
