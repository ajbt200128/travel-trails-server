# run `sudo ./quick-start.sh`
# runs colmap interactively

podman pull colmap/colmap:latest
podman run --name colmap_cont --security-opt seccomp=unconfined --gpus all -w /working -v /:/working -it colmap/colmap:latest
#podman exec -it colmap_cont /working/home/jonathanlee/colmap/docker/entrypoint.py >> /home/jonathanlee/colmap_log.txt
#podman stop colmap_cont
#podman rm colmap_cont

