from flask import Flask, send_file, request
from flask_cors import CORS
from pytubefix import YouTube, Search

from utils import video_details_serializer, check_storage, TEMP_PATH

app = Flask(__name__)
CORS(app, origins=['*'])


@app.route("/", methods=["GET"])
def index():
    return {"message": "App is running."}


@app.route("/preview", methods=["GET"])
def preview():
    url = request.args.get("url")
    youtube = YouTube(url)
    return video_details_serializer(youtube.vid_info["videoDetails"])


@app.route("/search", methods=["GET"])
def search():
    search_query = request.args.get("search")
    search_results = Search(search_query)
    return [video_details_serializer(item.vid_info["videoDetails"]) for item in search_results.videos]


@app.route("/download", methods=["GET"])
def download():
    check_storage()
    url = request.args.get("url")
    youtube = YouTube(url)
    stream = youtube.streams.filter(only_audio=True).first()
    filename = f"{stream.title}.mp3"
    stream.download(output_path=TEMP_PATH, filename=filename)
    response = send_file(f"{TEMP_PATH}/" + filename)
    return response
