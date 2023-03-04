# run `sudo ./automatic-reconstruction.sh`
podman pull colmap/colmap:latest
podman run --name colmap_cont --security-opt seccomp=unconfined -td --gpus all -w /working -v /:/working colmap/colmap:latest
podman exec -it colmap_cont apt-get update && apt-get install python3-pip -y && pip3 install --upgrade pip && pip3 install opencv-python==4.3.0.38 && /working/home/jonathanlee/travel-trails-server/tt-server/server/colmap_entrypoint.py >> /home/jonathanlee/colmap_log.txt
#podman run --name colmap_cont --security-opt seccomp=unconfined -it --gpus all -w /working -v /:/working colmap/colmap:latest /bin/bash 
#podman exec -it colmap_cont apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub && apt-get update && apt-get install python3-pip -y && pip3 install --upgrade pip && pip3 install opencv-python==4.3.0.38 && /working/home/jonathanlee/travel-trails-server/tt-server/server/colmap_entrypoint.py >> /home/jonathanlee/colmap_log.txt
#podman exec -it colmap_cont apt-get install -y wget && apt-key del 7fa2af80 && wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && dpkg -i cuda-keyring_1.0-1_all.deb && apt-get update && apt-get install python3-pip -y && pip3 install --upgrade pip && pip3 install opencv-python==4.3.0.38 && /working/home/jonathanlee/travel-trails-server/tt-server/server/colmap_entrypoint.py >> /home/jonathanlee/colmap_log.txt
podman stop colmap_cont
podman rm colmap_cont
