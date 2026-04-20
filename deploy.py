from __future__ import annotations

from datetime import timedelta
from airflow.decorators import task
from airflow.models import Param
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from modules.tasks.credentials import get_credentials_task

with DAG(
    "Deploy",
    default_args={"retries": 0},
    params={"date_str": Param(default='2024_12_03_13_19_15', type="string")},
    description="Deploy PCA model to Modal.com",
    schedule=None,
    start_date=None,
    catchup=False,
    tags=["deploy"],
) as dag:
    setup_credentials = get_credentials_task()

    @task.bash
    def install_modal_cli() -> str:
        return 'pip install modal && rm ~/.modal.toml 2>/dev/null || true'

    @task.bash
    def setup_modal_token():
        return ("modal token set "
                "--token-id '{{ var.value.AIRFLOW_VAR_MODAL_TOKEN }}' "
                "--token-secret '{{ var.value.AIRFLOW_VAR_MODAL_SECRET }}'")

    @task.virtualenv(requirements='modules/requirements/deploy.txt')
    def download_model(params: dict):
        from modules.tasks.deploy import download_and_upload_to_volume
        download_and_upload_to_volume(params=params)

    deploy_on_modal = BashOperator(
        task_id='deploy_on_modal',
        bash_command=(
            "cp /opt/airflow/dags/repo/modules/app.py /tmp/app.py && "
            "sed -i 's/DATE_STR/{{ params.date_str }}/g' /tmp/app.py && "
            "modal deploy /tmp/app.py"
        ),
    )

    install = install_modal_cli()
    token = setup_modal_token()
    download = download_model()

    install >> token >> download
    setup_credentials >> download
    download >> deploy_on_modal
