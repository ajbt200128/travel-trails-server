import os
import json
import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from flask_migrate import Migrate
from server.image_tools import create_image_gallery, flickr_search

app = Flask(__name__, static_folder="/data")



# ===============================================================================
# Dashboard
# ===============================================================================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    # Get the locations
    locations = Location.query.all()
    locations = [location.to_dict() for location in locations]

    print(locations)
    print("printed locations")

    return render_template("index.html", locations=locations)


@app.route("/dashboard/createmodel", methods=["GET","POST"])
def dashboard_createmodel():
    if request.method == 'GET':
        return render_template("createmodel.html")

    elif request.method == 'POST':

        if "query" in request.form:
            flickr_query={}
            # TODO VALIDATE FORM FIELDS
            flickr_query["latitude"] = request.form["flickr_latitude"]
            flickr_query["longitude"] = request.form["flickr_longitude"]
            flickr_query["radius"] = request.form["flickr_radius"]
            flickr_query["tag"] = request.form["flickr_tag"]
        
            print("cwd: " + os.getcwd())
            ls_str = ' '.join([str(elem) for elem in os.listdir()])
            print("ls: " + ls_str)
        
            try:
                # read API key from file
                with open("api_keys.json") as f:
                    keys = json.load(f)
                    if "flickr_api_key" in keys:
                        flickr_api_key = str(keys["flickr_api_key"])
                    else:
                        raise ValueError("flickr_api_key not found in api_keys.json")
            except Exception as e:
                raise e

            try:
                # read API key from file
                with open("/data/api_keys.json") as f:
                    keys = json.load(f)
                    if "flickr_api_key" in keys:
                        flickr_api_key = str(keys["flickr_api_key"])
                    else:
                        raise ValueError("flickr_api_key not found in api_keys.json")
            except Exception as e:
                raise e



            # get photo urls at query
            photo_urls = flickr_search(
                api_key=flickr_api_key, parameters=flickr_query
            )

            return render_template("createmodel.html", query_results=request.form, photo_urls=photo_urls)

        elif "submit" in request.form: 
            return render_template("createmodel.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")