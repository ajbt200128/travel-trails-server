## How to use COLMAP:

### Setup

1. Check that Docker >=19.03<sup>[2](#f2)</sup> installed on your host machine:

`docker --version`

2. Check that you have an NVIDIA driver installed on your host machine

`nvidia-smi`

3. Setup the nvidia-toolkit on your host machine.

For Ubuntu host machines: `./setup-ubuntu.sh`. Seems to still work on unsupported distributions.

### Creating Dense Reconstruction

1. Put images into a directory. E.g. `~/gerrard/images`
2. `cd ~/colmap/docker`
3. Run the _quick-start_ script, using the _full local path_ to your prefered
   local working directory (a folder with your input files/images, etc.). This will open an interactive Docker container.
   `sudo ./quick-start.sh ~/`
4. Inside the container, use the CLI to run COLMAP with the automatic reconstructor:
   `colmap automatic_reconstructor --image_path /working/gerrard/images --workspace_path /working/gerrard`
5. Use `ctrl d` to disconnect.

## COLMAP Progress Updates:

- **11/12/22** Image dataset FTPed to Coltrane, mounted to container data. Feature detection works in container. However, dense reconstruction requires CUDA and GPU support, which is not included in the pre-built colmap package, it needs to be built from source. Additionally the Docker image should use `devel` instead of `base` because it includes `nvidia-continer-toolkit`.
- **11/13/22** Attempted to build Colmap in Dockerfile using RUN commands taken from these two sources. However, both resulted in the following build errors documented in [issue 1418](https://github.com/colmap/colmap/issues/1418) and [issue 862](https://github.com/colmap/colmap/issues/862). Tried changing c++ version to 14, and downgrading CUDA and Ubuntu version, to no avail.
  - [COLMAP Dockerfile](https://github.com/colmap/colmap/blob/dev/docker/Dockerfile)
  - [COLMAP in Docker](https://github.com/Kai-46/colmap_in_docker/blob/master/Dockerfile)
- **11/13/22** Dense reconstruction success!
  - Followed instructions in [COLMAP docker quick start](https://github.com/colmap/colmap/tree/dev/docker)
  - Used COLMAP CLI documented [here](https://colmap.github.io/cli.html)
  - Took 30-40 minutes to generate dense reconstruction from 100 images of Gerrard Hall (UNC CH)
