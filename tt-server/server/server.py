import uuid
from pathlib import Path

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.database import db
from server.models import *  # NOQA

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["UPLOAD_FOLDER"] = "/data"

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello, World!"}), 200


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
