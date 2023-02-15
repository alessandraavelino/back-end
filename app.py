from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from helpers.database import db, migrate
from model.download import Download
from resources.download import DownloadResource
# CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pweb:123456@localhost:5432/aemotor"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/songslicer"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



download = Download("email@gmail.com", "Venha se cadastrar no nosso aplicativo", "teste")
print(download)
db.init_app(app)
migrate.init_app(app, db)

api = Api(app)
api.add_resource(DownloadResource, '/downloads')


if __name__ == '__main__':
    app.run(debug=False)