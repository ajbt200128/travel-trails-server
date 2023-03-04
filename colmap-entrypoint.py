#!/usr/bin/python3.6

import os
import time
import glob
import shutil
import datetime
import subprocess
from subprocess import PIPE
from pathlib import Path

def printt(msg):
    now = datetime.datetime.now()
    print("[{}] {}".format(str(now),str(msg)))

'''
Automatically reconstructs model based on location_id

'''
def auto_reconstruct(location_id):
    now = datetime.datetime.now()
    print("==========[{}]==========".format(str(now)))

    printt("Executing colmap on location_id:{}".format(str(location_id)))

    start_time = time.time()

    # automatically reconstruct 
    command = [
        "colmap", 
        "automatic_reconstructor",
        "--image_path",
        "/working/var/travel-trails-files/images/{}".format(str(location_id)),
        "--workspace_path",
        "/working/var/travel-trails-files/models/{}".format(str(location_id)),
    ]

    out = subprocess.run(command, stdout=PIPE, stderr=PIPE)
    printt(out.returncode)
    printt(out.stdout.decode('utf-8'))

    total_time = time.time() - start_time
    printt("MODEL UPDATE COMPLETED IN {} SECONDS".format(str(total_time)))

    printt("==========[Done]==========")

def process_new_media(location_id):
    
    raw_img = Path("/working/var/travel-trails-files/") / "raw" / str(location_id) / "images"
    printt("Raw image path: {}".format(str(raw_img)))
    if (os.path.exists(str(raw_img))):
        # Move images into dest dir
        dest_dir = Path("/working/var/travel-trails-files/") / "images" / str(location_id)
        dest_dir.mkdir(parents=True, exist_ok=True)


        img_query = "{}/*.jpg".format(str(raw_img))
        imgs = glob.glob(img_query)
        if (len(imgs) == 0):
            printt("No images found")
        for img in imgs:
            img_name = img.split("/")[-1]
            dest_img = os.path.join(dest_dir,img_name)
            printt("Moving {} to {}".format(str(img), dest_img))
            shutil.move(str(img), str(dest_img))

    else:
        printt("Path does not exist: {}".format(str(raw_img)))

    raw_vid = Path("/working/var/travel-trails-files/") / "raw" / str(location_id) / "video"
    # Process videos
    raw_img = Path("/working/var/travel-trails-files/") / "raw" / str(location_id) / "images"
    printt("Raw image path: {}".format(str(raw_img)))
    if (os.path.exists(str(raw_img))):
        # Move images into dest dir
        dest_dir = Path("/working/var/travel-trails-files/") / "images" / str(location_id)
        dest_dir.mkdir(parents=True, exist_ok=True)


        img_query = "{}/*.jpg".format(str(raw_img))
        imgs = glob.glob(img_query)
        if (len(imgs) == 0):
            printt("No images found")
        for img in imgs:
            img_name = img.split("/")[-1]
            dest_img = os.path.join(dest_dir,img_name)
            printt("Moving {} to {}".format(str(img), dest_img))
            shutil.move(str(img), str(dest_img))

    else:
        printt("Path does not exist: {}".format(str(raw_img)))


if __name__ == "__main__":

    location_ids = [5]#, 5, 6, 7]
    for id in location_ids:
        printt("Processing id {}".format(str(id)))
        process_new_media(id)
        #model_filename = "{}_1.gltf".format(str(id))
        #auto_reconstruct(id, model_filename)