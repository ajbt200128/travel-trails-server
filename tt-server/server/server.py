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
