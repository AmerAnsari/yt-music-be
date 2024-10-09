import json
from typing import Tuple, NamedTuple

import nodejs
from flask import Flask, send_file, request
from flask_cors import CORS
from pytubefix import YouTube, Search

from utils import video_details_serializer, check_storage, TEMP_PATH

app = Flask(__name__)
CORS(app, origins=['*'])


class PoToken(NamedTuple):
    visitorData: str
    poToken: str


def token_verifier(token: PoToken) -> Tuple[str, str]:
    visitor_data = token.visitorData
    po_token = token.poToken
    return visitor_data, po_token


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

    output = nodejs.run(['bin/generate-po-token.js'], capture_output=True)
    token = json.loads(output.stdout.decode('utf-8'))
    po_token = PoToken(**token)

    search_results = Search(search_query, use_po_token=True, po_token_verifier=token_verifier(po_token))
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
