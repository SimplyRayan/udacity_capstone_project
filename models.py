import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

import os


database_name = "capstone"
if 'DATABASE_URL' in os.environ:
    DATABASE_URL = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
else:
    DATABASE_URL = "postgresql://postgres:postgres@{}/{}".format(
        'localhost:5432', database_name)


db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_URL, testing=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_and_create_all():
    db.drop_all()
    db.create_all()
    add_dummy_data()


def add_dummy_data():
    c1 = Collection(title="Nature", description="photos of nature")
    c2 = Collection(title="Movies", description="photos about movies")
    img1 = Image(title="Waterfall", image_link="linkt to image")
    img2 = Image(title="Desert Dunes", image_link="linkt to image..")
    img3 = Image(title="The Godfather Poster", image_link="linkt to image..")

    c1.images.append(img1)
    c1.images.append(img2)
    c2.images.append(img3)

    c1.insert()
    c2.insert()


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    images = db.relationship(
        'Image', backref="collection", lazy=True, cascade="all, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'images_count': len(self.images)
        }


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collection.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_link': self.image_link,
            'collection_title': self.collection.title
        }
