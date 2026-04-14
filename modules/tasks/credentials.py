import json
import os

from airflow.operators.python import PythonOperator


def setup_credentials():
    """Write GCP credentials file and set the env var pointing to it."""
    from airflow.models import Variable
    creds_path = Variable.get('AIRFLOW_VAR_GOOGLE_APPLICATION_CREDENTIALS')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
    credentials_dict = Variable.get('GOOGLE_CREDENTIALS_AUTHORIZATION', deserialize_json=True)
    with open(creds_path, 'w') as f:
        json.dump(credentials_dict, f)


def get_credentials_task():
    return PythonOperator(
        task_id="setup_credentials",
        python_callable=setup_credentials,
    )
