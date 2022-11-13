import pathlib

import pycolmap
from flask import Flask, jsonify
from flask_migrate import Migrate
from server.database import db
from server.models import *  # NOQA

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello, World!"})


@app.route("/genmodel")
def colmap():
    image_dir = pathlib.Path("/var/travel-trails-files/images/gerrard/")
    output_path = pathlib.Path("/var/travel-trails-files/models/gerrard")

    output_path.mkdir()
    mvs_path = output_path / "mvs"
    database_path = output_path / "database.db"

    pycolmap.extract_features(database_path, image_dir)
    pycolmap.match_exhaustive(database_path)
    maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
    maps[0].write(output_path)
    # dense reconstruction
    pycolmap.undistort_images(mvs_path, output_path, image_dir)
    pycolmap.patch_match_stereo(mvs_path)  # requires compilation with CUDA
    pycolmap.stereo_fusion(mvs_path / "dense.ply", mvs_path)
    return jsonify({"message": "Generated model successfully!"})
