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

Create a directory for postgres and models/images

```bash
sudo mkdir /var/travel-trails
sudo mkdir /var/travel-trails-data
```

Start server

```bash
./server-run.sh
```

Stop server

```bash
./server-down.sh
```

## COLMAP Container
```bash
sudo yum install -y nvidia-container-toolkit
```
Quiet message about Emulate Docker CLI with Podman
```bash
sudo touch /etc/containers/nodocker
```

Run colmap container (non-interactive)
```bash
sudo ./run-colmap-container.sh /home/jonathanlee
```

Run colmap container (interactive)
```bash
sudo ./run-colmap-container-interactive.sh /home/jonathanlee
```

Check podman container is actually removed
```bash
sudo podman container ls
```

## Update
To manually run Dockerfile, do
```bash
sudo podman run -f ./Dockerfile
```