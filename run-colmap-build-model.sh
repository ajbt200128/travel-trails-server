# Start a container with colmap, non-interactive, and mounting the argument as a volume to the /working directory 
docker pull colmap/colmap:latest
docker run --name colmap_container --security-opt seccomp=unconfined -td --gpus all -w /working -v $1:/working -it colmap/colmap:latest

# Do something with colmap
# TODO: add redirect to a log file????
docker exec colmap_container colmap automatic_reconstructor --image_path $2 --workspace_path $3 # >> 

# Stop and remove container
docker stop colmap_container 
docker rm colmap_container 
