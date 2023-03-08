import sys
import json
import datetime
import threading
import subprocess
from time import sleep
from flask import Flask, jsonify, request

app = Flask(__name__)

jobQueue = []
jobRun = []
jobDone = []

@app.route("/hello")
def hello():
    return jsonify({"message": "This is the colmap server!"}), 200

@app.route("/jobstatus", methods=["GET"])
def jobstatus():
    print("Printing job status")
    print("jobQueue: {}".format(jobQueue))
    print("jobRun: {}".format(jobRun))
    print("jobDone: {}".format(jobDone))
    return jsonify({"jobQueue": jobQueue, "jobRun": jobRun, "jobDone":jobDone}), 200

@app.route("/jobadd", methods=["POST"])
def jobadd():
    job = request.json()
    print("Received new job: {}", str(job))

    jobQueue.append(job)

    return jsonify({"message": jobQueue}), 200


def dojobs():
    while True:
        # Check queue for new job every 10 seconds
        sleep(10) 
        now = str(datetime.datetime.now())

        if (len(jobQueue) > 0):
            print("[{}] Found job in job queue".format(now))
            job = jobQueue.pop()
            jobRun.append(job)

            print("[{}] Job: {}".format(now,str(job)))

            if (job["type"] == "RECONSTRUCT"):
                location_id = job["location_id"]


                # TODO: Save the previous model before overwritting


                # Run colmap autoreconstruct

                command = [
                    "colmap",
                    "automatic_reconstructor",
                    "--image_path",
                    "/data/var/travel-trails-files/images/{}/images".format(str(location_id)),
                    "--workspace_path",
                    "/data/var/travel-trails-files/images/{}".format(str(location_id)),
                ]
                
                out = subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr)
                subprocess.wait()
                print("\n\n\n\n\n\n\n\n\n\n")
                now = str(datetime.datetime.now())
                print("[{}] Completed job {}".format(now, location_id))
                print("Return status: {}".format(out.returncode))
                print("\n\n\n\n\n\n\n\n\n\n")

                jobDone.append(jobRun.pop())

            if (job["type"] == "CONVERT"):
                # TODO: Potentially provide support for Austin's converter tool
                pass

        else:
            print("[{}] No jobs found in job queue".format(now))




if __name__ == "__main__":
    print("starting main")
    
    # start a job thread
    threading.Thread(target=dojobs).start()

    app.run(debug=True, use_reloader=False)
