import os
import json
import datetime
import requests
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from flask_migrate import Migrate
from server.constants import DATABASE_URL, UPLOAD_FOLDER
from server.converter import convert_ply
from server.database import db
from server.image_tools import create_image_gallery, flickr_search
from server.models import Image, Location  # NOQA
from server.utils import *

app = Flask(__name__, static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello, World!"}), 200


@app.route("/ping")
def ping():
    return jsonify({"message": "pong"}), 200


# ===============================================================================
# Location API
# ===============================================================================


@app.route("/locations", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    return jsonify([location.to_dict() for location in locations]), 200


@app.route("/location", methods=["POST"])
def create_location():
    data = request.get_json()
    if data is None:
        return jsonify({"message": "Invalid data"}), 400

    # Pairs of Lat/Lon points
    points = data.get("points")
    name = data.get("name")
    description = data.get("description")
    print(data, points, name, description)
    if points is None or name is None or description is None:
        return jsonify({"message": "Invalid data"}), 400
    location = Location.from_points(
        name=name,
        points=points,
        description=description,
        last_updated=datetime.datetime.now(),
    )
    db.session.add(location)
    db.session.commit()
    return jsonify(location.to_dict()), 201


@app.route("/location/<location_id>", methods=["GET"])
def get_location(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404
    return jsonify(location.to_dict()), 200


@app.route("/location/<location_id>/model.gltf", methods=["GET"])
def get_location_model(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404

    # open location.model_path and return it
    return send_file(location.model_path, mimetype="text/json"), 200


@app.route("/location/<location_id>", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404
    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted"}), 200


@app.route("/location/<location_id>/images", methods=["GET"])
def get_location_images(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404
    return jsonify([image.to_dict() for image in location.images]), 200


@app.route("/locations/nearby", methods=["GET"])
def nearby():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = request.args.get("radius")
    print(lat, lon, radius)
    if lat is None or lon is None:
        return jsonify({"message": "Invalid data"}), 400
    if radius is None:
        radius = 1000
    locations = Location.get_nearby(float(lat), float(lon), float(radius))
    return jsonify([location.to_dict() for location in locations]), 200


# ===============================================================================
# Image API
# ===============================================================================


@app.route("/upload_image/<location_id>", methods=["POST"])
def upload_file(location_id):
    uploaded_file = request.files["file"]
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404
    if uploaded_file:
        extension = Path(uploaded_file.filename or "file.png").suffix

        image = Image(
            location_id=location.id,
            date_uploaded=datetime.datetime.now(),
            extension=extension,
        )
        db.session.add(image)
        db.session.commit()
        path = image.path
        path.parent.mkdir(parents=True, exist_ok=True)
        uploaded_file.save(path)
        return jsonify(image.to_dict()), 201
    else:
        return jsonify({"success": False, "message": "no file"}), 400


@app.route("/image/<image_id>", methods=["GET"])
def get_image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    return send_file(image.path), 200


@app.route("/image/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200


@app.route("/image/<image_id>/data", methods=["GET"])
def get_image_data(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return jsonify({"message": "Image not found"}), 404
    return jsonify(image.to_dict()), 200


# ===============================================================================
# Dashboard
# ===============================================================================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    # Get the locations
    locations = Location.query.all()
    locations = [location.to_dict() for location in locations]

    #print(locations)
    #print("printed locations")

    return render_template("index.html", locations=locations)


@app.route("/dashboard/createmodel", methods=["GET","POST"])
def dashboard_createmodel():
    if request.method == 'GET':
        return render_template("createmodel.html")

    elif request.method == 'POST':
        # All fields are required
        name = request.form["name"]
        desc = request.form["description"]
        lat = request.form["latitude"]
        lon = request.form["longitude"]

        # Entry validation
        valid = True
        if (not isinstance(name,str) or not (name and name.strip())):
            # name is not a string or it is none, empty, or blank
            print("Error parsing name:")
            print(str(name))
            valid = False

        if (not isinstance(desc,str) or not (desc and desc.strip())):
            # desc is not a string or it is none, empty, or blank
            print("Error parsing desc:")
            print(str(desc))
            valid = False

        if (not is_float(lat) or
            not (float(lat) >= -180.0 and float(lat) <= 180.0)):
            # lat is not a float or not in valid range [0, 180]
            print("Error parsing lat:")
            print(str(lon))
            valid = False

        if (not is_float(lon) or
            not (float(lon) >= -180.0 and float(lon) <= 180.0)):
            # lon is not a float or not in valid range [0, 180]
            print("Error parsing lon:")
            print(str(lon))
            valid = False

        if not valid:
            return render_template("createmodel.html",msg="Error creating model.")
        else:
            # Add the location

            # Compute a square around the center lat, lon
            radius = 0.0001 # about 60 ft
            lat = float(lat)
            lon = float(lon)
            points = [
                (lat - radius, lon - radius),
                (lat - radius, lon + radius),
                (lat + radius, lon + radius),
                (lat + radius, lon - radius),
            ]
            
            # NOTE: This is just chopped from /locations route
            location = Location.from_points(
                name=name,
                points=points,
                description=desc,
                last_updated=datetime.datetime.now(),
            )
            db.session.add(location)
            db.session.commit()

            return render_template("createmodel.html",msg="Created model successfully.")

@app.route("/dashboard/addmedia/<location_id>", methods=["GET","POST"])
def dashboard_addmedia(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return render_template("addmedia.html",msg="Invalid location id.")
    else:
        location = location.to_dict()

    if request.method == 'GET':
        return render_template("addmedia.html",location=location)

    elif request.method == 'POST':

        if "query" in request.form:
            flickr_query={}
            # TODO VALIDATE FORM FIELDS
            flickr_query["latitude"] = request.form["flickr_latitude"]
            flickr_query["longitude"] = request.form["flickr_longitude"]
            flickr_query["radius"] = request.form["flickr_radius"]
            flickr_query["tag"] = request.form["flickr_tag"]
        
            try:
                # Read API key from file
                with open("/data/api_keys.json") as f:
                    keys = json.load(f)
                    if "flickr_api_key" in keys:
                        flickr_api_key = str(keys["flickr_api_key"])
                    else:
                        raise ValueError("flickr_api_key not found in api_keys.json")
            except IOError as e:
                print("Add api_keys.json to /var/travel-trails-files")
                raise e
            except Exception as e:
                raise e


            # Get photo urls at query
            photo_urls = flickr_search(
                api_key=flickr_api_key, parameters=flickr_query
            )

            return render_template("addmedia.html",location=location, msg="Query was pressed", query_results=flickr_query, photo_urls=photo_urls)

        elif "add" in request.form: 

            # Check if image was submitted
            image = request.files["image"]
            if (image.filename and image.filename != ""):
                print("Received image")
                print(image.filename)

                # Create a path
                path = Path(UPLOAD_FOLDER) / "raw" / str(location["id"]) / "images" / str(image.filename)
                path.parent.mkdir(parents=True, exist_ok=True)
                image.save(path)

            # Check if video was submitted
            video = request.files["video"]
            if (video.filename and video.filename != ""):
                print("Received video")
                print(video.filename)

                # Create a path
                path = Path(UPLOAD_FOLDER) / "raw" / str(location["id"]) / "videos" / str(video.filename)
                path.parent.mkdir(parents=True, exist_ok=True)
                video.save(path)

            # Check if Flickr data
            if ("photo_urls" in request.form and request.form["photo_urls"] != ""):
                print(request.form["photo_urls"])
                photo_urls = request.form["photo_urls"]
                photo_urls = [i.strip() for i in request.form["photo_urls"][1:-1].replace("'","").split(',')]
                print("Photos selected: {}".format(len(photo_urls)))

                # Loop over each photo url and save it to path
                # TODO: Checkboxes are not unchecked
                for url in photo_urls:

                    # Write to file
                    filename = url.split("/")[-1]
                    path = Path(UPLOAD_FOLDER) / "raw" / str(location["id"]) / "images" / filename
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'wb') as f:
                        print("Writing to {}".format(str(path)))
                        f.write(requests.get(url).content)

            # Download the media to the raw directory
            return render_template("addmedia.html", msg="Media was successfully added to server", location=location)
        
        return render_template("addmedia.html", msg="Error, POST form invalid", location=location)

