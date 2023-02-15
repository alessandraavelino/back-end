
from flask_restful import (Resource, current_app, marshal, marshal_with,
                           reqparse)
from sqlalchemy import exc
from pytube import YouTube
from moviepy.editor import *
import moviepy.editor as mp
import re
import os

from helpers.database import db
from model.download import Download, download_fields
from model.error import Error, error_campos
from model.utils import Utils
parser = reqparse.RequestParser()

parser.add_argument('link', required=True)
parser.add_argument('initial_time', required=True)
parser.add_argument('final_time', required=True)

    
class DownloadResource(Resource):
    @marshal_with(download_fields)
    def get(self):
        current_app.logger.info("Get - Downloads")
        download = Download.query.all()
        return download, 200
    
    def post(self):
        current_app.logger.info("Post - Downloads")
        try:
            # JSON
            args = parser.parse_args()
            current_app.logger.info("Post - Downloads")
            
            link = args['link']
            initial_time = args['initial_time']
            final_time = args['final_time']

            
            yt = YouTube(link)
            ys = yt.streams.filter(only_audio=True).first().download("Downloads")

            for file in os.listdir("Downloads"):
                if re.search("mp4", file):
                    mp4_path = os.path.join("Downloads", file)
                    mp3_path = os.path.join("Downloads", os.path.splitext(file)[0]+".mp3")
                    new_file = mp.AudioFileClip(mp4_path)
                    new_file.write_audiofile(mp3_path)
                    os.remove(mp4_path)
                print("sucesso!")

            audio = AudioFileClip(mp3_path)
            fstart_time = Utils.converter(initial_time)
            fend_time = Utils.converter(final_time)
            trimed_video = audio.subclip(fstart_time, fend_time)

            trimed_video.write_audiofile(f"Downloads/baixado.mp3")
            print("teste após trimed")

            download = Download(link, initial_time, final_time)

            db.session.add(download)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = Error(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                         err.__cause__())
            return marshal(erro, error_campos), 500

        return [{"message": "A música foi baixada e editada com sucesso!"}, 204]


# link = input("Digite o link do vídeo: ")
# path = input("Digite o diretório pra salvar: ")
