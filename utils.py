import math
import os
import re
import shutil
from datetime import timedelta

TEMP_PATH = "temp"


def check_storage():
    if len(os.listdir(TEMP_PATH)) > 10:
        shutil.rmtree(TEMP_PATH)


def format_count(count):
    count = int(count)  # Convert count to integer if it's a string
    suffixes = ['', 'k', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if count < 1000:
        return str(count)
    exp = int((len(str(abs(count))) - 1) / 3)
    formatted_count = math.floor(count / (1000 ** exp) * 10) / 10
    return f'{formatted_count}{suffixes[exp]}'


def format_seconds(seconds):
    time = str(timedelta(seconds=int(seconds)))
    parts = time.split(":")
    if parts[0] is '0':
        return ":".join([parts[1], parts[2]])
    else:
        return time


def video_details_serializer(info):
    keys = [
        "title",
        "videoId",
        "channelId",
        "author",
    ]
    obj = {}
    pattern = re.compile(r'(?<!^)(?=[A-Z])')

    obj["thumbnail"] = max(info["thumbnail"]["thumbnails"], key=lambda item: item["height"])["url"]
    obj["view_count"] = format_count(info['viewCount'])
    obj["time"] = format_seconds(info['lengthSeconds'])

    for key in keys:
        if key in info:
            obj[pattern.sub('_', key).lower()] = info[key]
    return obj
