"""Models for divercity app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import get_flashed_messages
from sqlalchemy import desc
from datetime import datetime
import flickrapi

db = SQLAlchemy()


class User(db.Model):
    """A list of users."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Collection(db.Model):
    """A collection that stores images."""

    __tablename__ = 'collections'

    collection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_saved = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(2000), nullable=True)

    users = db.relationship('User', backref='collections')
    pictures = db.relationship('Picture', backref='collections')


    def __repr__(self):
        return f'<Collection collection_id={self.collection_id} user={self.user_id}>'


class Picture(db.Model):
    """A picture."""

    __tablename__ = 'pictures'

    picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.collection_id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return f'<Picture picture_id={self.picture_id} URL={self.url}>'


def connect_to_db(flask_app, db_uri='postgresql:///images', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
