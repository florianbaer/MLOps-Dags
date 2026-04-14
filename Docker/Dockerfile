FROM apache/airflow:2.10.0-python3.9
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim build-essential g++ \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir "apache-airflow[uv]==2.10.0"