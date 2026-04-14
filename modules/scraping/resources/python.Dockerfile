FROM python:3.12.7 as playwright
ARG UID
ARG GID

USER root

RUN apt-get update && apt-get install -y python3-pip libevdev-dev wget git


ENV PATH="/usr/local/bin/playwright:/usr/local/bin:${PATH}"

RUN pip3 install --upgrade pip
RUN pip3 install pypi
RUN pip3 install playwright --no-cache-dir

RUN python -m playwright install
RUN playwright install-deps
RUN playwright install

# create user with uid and gid
# create group with gid
RUN groupadd -g ${GID} user
RUN useradd -m -u ${UID} -g ${GID} user
ENV PYTHONPATH "${PYTHONPATH}:/app/main/"

USER user

ENV PATH="/home/user/.local/bin:${PATH}"

FROM playwright as python

# install requirements
COPY resources/requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt


COPY resources/credentials.json /app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

CMD ["/bin/bash"]