FROM colmap/colmap:latest
WORKDIR /colmap-server
VOLUME /data
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub
RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y --fix-missing
RUN apt install -y python3.9 python3.9-distutils python3-pip netcat curl  libgl1
RUN python3.9 -m pip install --upgrade setuptools pip distlib
RUN python3.9 -m pip install poetry

COPY pyproject.toml poetry.lock ./
COPY colmap-server ./colmap-server
COPY entrypoint.sh ./
COPY run-colmap-build-model.sh ./


RUN poetry install --no-dev


CMD ["poetry", "run", "./entrypoint.sh"]