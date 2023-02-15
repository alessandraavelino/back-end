from helpers.database import db
from flask_restful import fields

download_fields = {
    'id': fields.Integer(attribute='id'),
    'link': fields.String(attribute='link'),
    'initial_time': fields.String(attribute='initial_time'),
    'final_time': fields.String(attribute='final_time')
}
class Download(db.Model):
    __tablename__ = "tb_download"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200), nullable=False)
    initial_time = db.Column(db.String(8), nullable=False)
    final_time = db.Column(db.String(8), nullable=False)

    
    def __init__(self, link, initial_time, final_time):
        self.link = link
        self.initial_time = initial_time
        self.final_time = final_time


    def __repr__(self):
        return f'Downloads(link={self.link}, initial_time={self.initial_time}, final_time={self.final_time})'