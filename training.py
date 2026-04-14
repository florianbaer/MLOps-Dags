from __future__ import annotations

from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.models import Param
from airflow.models.dag import DAG
from modules.tasks.credentials import get_credentials_task

REQUIREMENTS = 'modules/requirements/training.txt'

with DAG(
    "Training",
    default_args={"retries": 0},
    params={"date_str": Param(default=datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), type="string")},
    description="Export data, compute embeddings, and train PCA model",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 12, 2, 12, 0, 0),
    catchup=False,
    tags=["training"],
) as dag:
    setup_credentials = get_credentials_task()

    @task.virtualenv(requirements=REQUIREMENTS, use_uv=True)
    def export_db(params: dict):
        from modules.tasks.export_db import db_export
        db_export(params)

    @task.virtualenv(requirements=REQUIREMENTS, use_uv=True)
    def preprocess_jobs(params: dict):
        from modules.tasks.preprocessing import preprocessing
        preprocessing(params)

    @task.virtualenv(requirements=REQUIREMENTS, use_uv=True)
    def training(params: dict):
        from modules.tasks.training import train
        train(params)

    setup_credentials >> export_db() >> preprocess_jobs() >> training()
