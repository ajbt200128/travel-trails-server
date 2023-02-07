import os
import json
import datetime
from pathlib import Path
from flask import Flask, render_template, request
from image_tools import create_image_gallery, flickr_search
'''
import os
import json
import datetime
from pathlib import Path

from flask_migrate import Migrate
from server.image_tools import create_image_gallery, flickr_search
'''

app = Flask(__name__, static_folder="static")


# ===============================================================================
# Dashboard
# ===============================================================================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    # Get the locations
   
    #locations = Location.query.all()
    #locations = [location.to_dict() for location in locations]
   
    locations = [{'id': 1, 'name': 'FDR Memorial', 'geometry': {'type': 'Polygon', 'coordinates': (((23.456, 45.678), (24.456, 48.678), (25.456, 49.678), (23.456, 45.678)),)}, 'latitude': 23.456, 'longitude': 45.678, 'description': 'A memorial to Franklin Delano Roosevelt', 'last_updated': datetime.datetime(2022, 12, 4, 19, 44, 10, 509732)}, {'id': 2, 'name': 'Washington Monument', 'geometry': {'type': 'Polygon', 'coordinates': (((38.889484, -77.035278), (38.889484, -77.035278), (38.889484, -77.035278), (38.889484, -77.035278)),)}, 'latitude': 38.889484, 'longitude': -77.035278, 'description': 'Washington mounument', 'last_updated': datetime.datetime(2023, 1, 31, 1, 7, 8, 673327)}] 

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
        
            try:
                # read API key from file
                with open("/var/travel-trails-files/api_keys.json") as f:
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

            print("photo_urls")
            print(photo_urls)
            
            return render_template("createmodel.html", query_results=request.form, photo_urls=photo_urls)

        elif "submit" in request.form: 
            return render_template("createmodel.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")