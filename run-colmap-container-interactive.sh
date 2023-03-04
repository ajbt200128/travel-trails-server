# sudo ./run-colmap-container.sh /home/jonathanlee

# Start a container with colmap, non-interactive, and mounting the argument as a volume to the /working directory 
docker pull colmap/colmap:latest
docker run --name colmap_container --security-opt seccomp=unconfined --gpus all -w /working -v $1:/working -it colmap/colmap:latest

# Stop and remove container
docker stop colmap_container 
docker rm colmap_container 
