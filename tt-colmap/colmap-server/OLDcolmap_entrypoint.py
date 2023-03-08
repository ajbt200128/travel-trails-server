#!/usr/bin/python3.6

import cv2
import os
import time
import glob
import shutil
import datetime
import subprocess
from subprocess import PIPE
from pathlib import Path

def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False



def printt(msg):
    now = datetime.datetime.now()
    print("[{}] {}".format(str(now),str(msg)))

NUM_FRAMES = 100 # extract 100 frames from each video

def save_video_frames(video_path, num_frames, dest_path):
    prefix = video_path.split("/")[-1].split(".")[0]

    # save frames of the video
    cap = cv2.VideoCapture(video_path)

    #length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    skip = 10#length / num_frames

    no_skip = False
    # if there are less frames in the video then what we request,
    # don't skip any frames
    # if (length < num_frames):
    #     no_skip = True

    i = 0
    j = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        #frame = cv2.resize(frame, (540,960))
        if (i % skip == 0):
            # for some reason, frame appears flipped
            frame = cv2.flip(frame, 0)
            frame_name = "{}_{}.jpg".format(prefix, str(j).zfill(5))
            frame_path = str(os.path.join(dest_path, frame_name))
            cv2.imwrite(frame_path,frame)
            print("wrote frame {}".format(frame_path))
            j += 1
        i += 1

    cap.release()
    cv2.destroyAllWindows()

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
        "/working/var/travel-trails-files/images/{}/images".format(str(location_id)),
        "--workspace_path",
        "/working/var/travel-trails-files/images/{}".format(str(location_id)),
    ]
    for c in command:
        printt(c)

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

    # Process videos
    raw_vid = Path("/working/var/travel-trails-files/") / "raw" / str(location_id) / "videos"
    printt("Raw video path: {}".format(str(raw_vid)))
    if (os.path.exists(str(raw_vid))):
        # Process each video and and split each frame into dest dir
        dest_dir = Path("/working/var/travel-trails-files/") / "images" / str(location_id)
        dest_dir.mkdir(parents=True, exist_ok=True)

        vid_query = "{}/*.mp4".format(str(raw_vid))
        vids = glob.glob(vid_query)
        if (len(vids) == 0):
            printt("No videos found")
        for vid in vids:
            # Process each frame
            printt("Processing video frames of {} and outputting to {}".format(vid,str(dest_dir)))
            save_video_frames(vid, NUM_FRAMES, dest_dir)

    else:
        printt("Path does not exist: {}".format(str(raw_vid)))


if __name__ == "__main__":

    location_ids = [5]#, 5, 6, 7]
    for id in location_ids:
        printt("Processing id {}".format(str(id)))
        process_new_media(id)
        #model_filename = "{}_1.gltf".format(str(id))
        auto_reconstruct(id)