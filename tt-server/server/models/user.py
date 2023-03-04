from pathlib import Path
from datetime import datetime

from server.database import db

class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    profile_picture = db.Column(db.String(1024), nullable=False)

    @classmethod
    def create(cls, username, name, profile_picture):
        user = cls(username=username, name=name, profile_picture=profile_picture)
        db.session.add(user)
        db.session.commit()
        return user

    @property
    def visits(self):
        visits = db.session.query(UserVisit).filter_by(username=self.username).all()
        return [visit.to_dict() for visit in visits]

    def to_dict(self):
        return {
            'username': self.username,
            'name': self.name,
            'profile_picture': self.profile_picture
        }


class UserVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey("user.username"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    time_visited = db.Column(db.DateTime, nullable=False)

    @classmethod
    def create(cls, username, location_id):
        time_visited = datetime.now()
        visit = cls(username=username, location_id=location_id, time_visited=time_visited)
        db.session.add(visit)
        db.session.commit()
        return visit

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'location_id': self.location_id,
            'time_visited': self.time_visited
        }
