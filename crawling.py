from __future__ import annotations

from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.models.dag import DAG

with DAG(
    "Crawling",
    default_args={"retries": 0},
    description="Crawl AI job postings from jobs.ch",
    schedule=timedelta(hours=4),
    start_date=datetime(2024, 12, 2, 12, 0, 0),
    catchup=True,
    tags=["crawling"],
) as dag:
    from modules.tasks.credentials import get_credentials_task

    setup_credentials = get_credentials_task()

    @task.virtualenv(requirements='modules/requirements/crawling.txt', use_uv=True)
    def crawling():
        from modules.tasks.credentials import setup_credentials
        setup_credentials()
        from modules.scraping.scripts.crawl_ai_jobs import Program
        import asyncio
        program = Program()
        asyncio.run(program.main())

    setup_credentials >> crawling()
