# Requirements

First make sure python and podman are installed.

Install poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
# inside folder
poetry install
```

Install pre-commit

```bash
pip install pre-commit
pre-commit install
```

To add python dependencies:

```bash
poetry add <dependency>
```

Install podman (or docker).

```bash
sudo apt install podman
```

Install nvidia compatibility layer (see [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) if not on Ubuntu):

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt install nvidia-container-toolkit
```

Create a directory for postgres

```bash
sudo mkdir /var/travel-trails
```

Start server

```bash
./server-run.sh
```
