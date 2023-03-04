apt-get update
apt-get install python3-pip -y 
pip3 install --upgrade pip 
pip3 install opencv-python==4.3.0.38 
pip3 install requests flask flask_migrate
/working/home/jonathanlee/travel-trails-server/tt-server/server/colmap_entrypoint.py >> /working/home/jonathanlee/colmap_log.txt