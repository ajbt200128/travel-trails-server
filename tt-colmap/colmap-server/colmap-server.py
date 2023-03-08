import threading
from time import sleep
from flask import Flask, jsonify
from multiprocessing import Process, Value

app = Flask(__name__)

@app.route("/hello")
def hello():
    return jsonify({"message": "Hello, this is the colmap server!"}), 200

def dojobs():
    while True:
        sleep(1)
        print("doing josdsfb")

if __name__ == "__main__":
    print("starting main")
    
    # start a job thread
    threading.Thread(target=dojobs).start()

    app.run(debug=True, use_reloader=False)
