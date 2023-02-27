from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import ResourceList, Api, ResourceDetail
from flask_cors import CORS
import json


with open('config.json', 'r') as file:
    settings = json.load(file)['settings']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
    settings['DB_USER'], settings['DB_PASS'], settings['DB_HOST'], settings['DB_PORT'], settings['DATABASE'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    genre = db.Column(db.String)
    image_url = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)


class ArtistSchema(Schema):
    class Meta:
        type_ = 'artist'
        self_view = 'artist_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artist_many'
    id = fields.Integer()
    name = fields.Str()
    birth_date = fields.Date(required=True)
    genre = fields.Str()
    image_url = fields.Str(required=True)
    description = fields.Str(required=True)


# fetch a list of artists
class ArtistMany(ResourceList):
    schema = ArtistSchema
    data_layer = {'session': db.session, 'model': Artist}


# fetch the details of a single artist
class ArtistOne(ResourceDetail):
    schema = ArtistSchema
    data_layer = {'session': db.session, 'model': Artist}


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    release_date = db.Column(db.String)
    description = db.Column(db.String)
    movie_genre = db.Column(db.String)
    


# http routes
api = Api(app)
api.route(ArtistMany, 'artist_many', '/artists')
api.route(ArtistOne, 'artist_one', '/artists/<int:id>')

if (__name__ == '__main__'):
    app.run(debug=True)