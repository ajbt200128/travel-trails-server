FROM colmap/colmap:latest
WORKDIR /server
VOLUME /data
ENV DEBIAN_FRONTEND=noninteractive

# Fix missing keyring
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-key del 7fa2af80
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

# setup python
RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install -y python3.9 python3.9-distutils python3-pip netcat
RUN python3.9 -m pip install --upgrade setuptools pip distlib
RUN python3.9 -m pip install poetry

COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY migrations ./migrations
COPY README.md ./
COPY entrypoint.sh ./

RUN poetry install --no-dev


CMD ["poetry", "run", "./entrypoint.sh"]
