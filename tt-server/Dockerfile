FROM nvidia/cuda:11.8.0-base-ubuntu22.04
WORKDIR /server
VOLUME /data
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y --fix-missing
RUN apt install -y python3.9 python3.9-distutils python3-pip netcat curl  libgl1
RUN curl -L https://github.com/isl-org/Open3D/releases/download/v0.16.0/open3d-0.16.0-cp39-cp39-manylinux_2_27_x86_64.whl --output /server/open3d-0.16.0-cp39-cp39-manylinux_2_27_x86_64.whl
RUN python3.9 -m pip install poetry

COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY migrations ./migrations
COPY README.md ./
COPY entrypoint.sh ./


RUN poetry install --no-dev


CMD ["poetry", "run", "./entrypoint.sh"]
