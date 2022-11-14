FROM nvidia/cuda:11.8.0-devel-ubuntu22.04
WORKDIR /server
VOLUME /data
ENV DEBIAN_FRONTEND=noninteractive

# install colmap and dependencies

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    vim

RUN apt-get update && apt-get install -y \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-regex-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    libmetis-dev \
    qtbase5-dev \
    libqt5opengl5-dev

RUN apt-get update && apt-get install -y \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libcgal-qt5-dev

RUN mkdir /tools

# install ceres-solver

WORKDIR /tools
RUN apt-get update && apt-get install -y libatlas-base-dev libsuitesparse-dev
RUN git clone https://ceres-solver.googlesource.com/ceres-solver
WORKDIR /tools/ceres-solver
#RUN git checkout $(git describe --tags)
RUN git checkout 783637a6ed285abc6c57b16ccd968c594a91b35f
RUN mkdir build
WORKDIR /tools/ceres-solver/build
RUN cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
RUN make -j4 && make install

# install colmap

WORKDIR /tools
RUN git clone https://github.com/colmap/colmap.git
WORKDIR /tools/colmap
RUN git checkout dev
RUN mkdir build
WORKDIR /tools/colmap/build
RUN   cmake .. \
        -DCUDA_ENABLED=ON \
        -DCUDA_NVCC_FLAGS="--std c++14" && \
        make -j$(( $(nproc) + 1 )) && make install
#RUN cmake ..
#RUN make -j4 && make install

# remove unneeded files
RUN rm -rf /tools

# other updates
RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install -y python3.9 python3.9-distutils python3-pip netcat
RUN python3.9 -m pip install poetry
RUN apt install ffmpeg libsm6 libxext6  -y

COPY pyproject.toml poetry.lock ./
COPY server ./server
COPY migrations ./migrations
COPY README.md ./
COPY entrypoint.sh ./

RUN poetry install --no-dev


CMD ["poetry", "run", "./entrypoint.sh"]
