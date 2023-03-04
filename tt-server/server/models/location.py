from pathlib import Path

from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from server.constants import UPLOAD_FOLDER
from server.converter import convert_ply
from server.database import db
from shapely import geometry
from shapely.geometry import Point, Polygon
from multiprocessing import Process

job_queue = []

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    geometry = db.Column(Geometry(geometry_type="POLYGON", srid=4326))
    description = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

    @property
    def images(self):
        return Image.query.filter_by(location_id=self.id).all()

    @property
    def point_cloud_path(self):
        return Path(UPLOAD_FOLDER) / "images" / f"{self.id}" / "dense" / "0" / "fused.ply"

    @property
    def model_path(self):
        return Path(UPLOAD_FOLDER) / "models" / f"{self.id}.gltf"

    @property
    def heatmap_path(self):
        return Path(UPLOAD_FOLDER) / "heatmaps" / f"{self.id}.gltf"

    @classmethod
    def from_points(cls, name, points, description, last_updated):

        # Create a polygon from the points
        points = [Point(p[0], p[1]) for p in points]
        polygon = Polygon([[p.x, p.y] for p in points])
        geometry = from_shape(polygon, srid=4326)
        location =  cls(
            name=name,
            geometry=geometry,
            description=description,
            last_updated=last_updated,
        )
        db.session.add(location)
        db.session.commit()
        return location

    @classmethod
    def get_nearby(cls, lat, lon, radius):
        point = Point(lat, lon)
        geometry = from_shape(point, srid=4326)
        return cls.query.filter(Location.geometry.ST_DWithin(geometry, radius)).all()

    @classmethod
    def check_queue(cls):
        current_jobs = [cls.query.get(job[1]).name for job in job_queue]
        print("Current queue:", current_jobs, flush=True)
        finished_jobs = []
        for (p, id) in job_queue:
            if not p.is_alive():
                job_queue.remove((p, id))
                finished_jobs.append(id)

        names = [cls.query.get(id).name for id in finished_jobs]
        return names

    def convert(self):
        p = Process(target=self.convert_process)
        p.start()
        job_queue.append((p, self.id))

    def convert_process(self):
        print("Converting location", self.id, flush=True)
        convert_ply(self.point_cloud_path, self.model_path)
        convert_ply(self.point_cloud_path, self.heatmap_path, heatmap=0.035)

    def to_dict(self):
        location_geometry = geometry.mapping(to_shape(self.geometry))
        return {
            "id": self.id,
            "name": self.name,
            "geometry": location_geometry,
            "latitude": location_geometry["coordinates"][0][0][0],
            "longitude": location_geometry["coordinates"][0][0][1],
            "description": self.description,
            "last_updated": self.last_updated,
        }


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)
    extension = db.Column(db.String(4), nullable=False)

    @property
    def name(self):
        return f"{self.id}{self.extension}"

    @property
    def path(self):
        return Path(UPLOAD_FOLDER) / "images" / f"{self.location_id}" / f"{self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "location_id": self.location_id,
            "date_uploaded": self.date_uploaded,
            "name": self.name,
        }
