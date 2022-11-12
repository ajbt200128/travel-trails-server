FROM nvidia/cuda:11.8.0-base-ubuntu22.04
WORKDIR /server
VOLUME /data
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install -y python3.9 python3.9-distutils python3-pip netcat
RUN python3.9 -m pip install poetry

COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY migrations ./migrations
COPY README.md ./
COPY entrypoint.sh ./

RUN poetry install --no-dev


CMD ["poetry", "run", "./entrypoint.sh"]
