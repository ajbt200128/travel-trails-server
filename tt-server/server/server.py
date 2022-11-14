import subprocess
import uuid
from pathlib import Path

import pycolmap
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.database import db
from server.models import *  # NOQA

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["UPLOAD_FOLDER"] = "/data"

# app.config["COLMAP_DATA"] = "/data"
db.init_app(app)

migrate = Migrate(app, db)

# GENERATE MODEL
# check for CUDA support
result = subprocess.run(
    ["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
print(result.stdout)
result = subprocess.run(["nvcc", "--version"], stdout=subprocess.PIPE, text=True)
print(result.stdout)

print("Generating Model")
image_dir = Path("/data/images/gerrard/")
output_path = Path("/data/models/gerrard")

output_path.mkdir(exist_ok=True)

mvs_path = output_path / "mvs"
database_path = output_path / "database.db"
print("Database_path: " + str(database_path))

# print("EXTRACT FEATURES")
# pycolmap.extract_features(database_path, image_dir)
# print("MATCH FEATURES")
# pycolmap.match_exhaustive(database_path)
# print("INCREMENTAL MAPPING")
# maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
# maps[0].write(output_path)
# # dense reconstruction
# print("DENSE RECONSTRUCTION PROCESS:")
# print("UNDISTORT IMAGES")
# pycolmap.undistort_images(mvs_path, output_path, image_dir)
print("PATCH MATCH STEREO")
pycolmap.patch_match_stereo(mvs_path)  # requires compilation with CUDA
print("STEREO FUSION")
pycolmap.stereo_fusion(mvs_path / "dense.ply", mvs_path)


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello, World!"})


@app.route("/genmodel")
def genmodel():
    return jsonify({"message": "Generated model successfully!"})


@app.route("/upload_image/<location_id>", methods=["POST"])
def upload_file(location_id):
    uploaded_file = request.files["file"]
    if uploaded_file:
        file_uuid = str(uuid.uuid4())
        path = Path(app.config["UPLOAD_FOLDER"]) / "images" / location_id
        path.mkdir(parents=True, exist_ok=True)

        uploaded_file.save(path / file_uuid)
        return (
            jsonify(
                {"success": True, "message": f"saved {location_id} to {file_uuid}"}
            ),
            200,
        )
    else:
        return jsonify({"success": False, "message": "no file"}), 400
