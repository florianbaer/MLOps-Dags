FROM quay.io/jupyter/minimal-notebook

ARG UID
ARG GID

USER root

RUN chown -R ${UID} /home/jovyan

RUN apt-get update && apt-get install -y python3-pip libevdev-dev wget git

USER ${NB_UID}


# install requirements
RUN pip install --upgrade pip
#USER ${NB_UID}:${DOCKER_GROUP}

RUN pip3 install pypi

COPY resources/requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN conda config --add channels conda-forge
RUN conda config --add channels microsoft
RUN conda install playwright -y

USER root

RUN playwright install --with-deps

USER ${NB_UID}

CMD ["/bin/bash"]
