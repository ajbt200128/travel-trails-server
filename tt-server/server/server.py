import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_migrate import Migrate
from server.constants import DATABASE_URL, UPLOAD_FOLDER
from server.converter import convert_ply
from server.database import db
from server.models import Image, Location  # NOQA

app = Flask(__name__)

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


@app.route("/location/<location_id>/model", methods=["GET"])
def get_location_model(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404

    convert_ply(location.point_cloud_path, location.model_path)
    return send_file(location.model_path, mimetype="application/octet-stream"), 200


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
