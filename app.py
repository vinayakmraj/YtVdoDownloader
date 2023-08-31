import os
import json
import requests
from flask import Flask, render_template, request
from pytube import YouTube
from moviepy.editor import VideoFileClip

app = Flask(__name__)

YOUTUBE_API_KEY = "AIzaSyD1J_mq4Vq7lSkSw3m69PK7cBSgQWYCftE"  # Replace with your API key

def get_video_info(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={YOUTUBE_API_KEY}&part=snippet"
    response = requests.get(url)
    data = json.loads(response.content)
    return data["items"][0]["snippet"]

def get_default_download_path():
    if os.name == "posix":  # Unix-like systems
        return os.path.expanduser("~/Downloads")
    elif os.name == "nt":   # Windows
        return os.path.expanduser("~/Downloads")
    else:
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()
        download_path = get_default_download_path()
        video_path = video_stream.download(output_path=download_path)

        video_info = get_video_info(yt.video_id)

        # Convert video to MP3
        video_clip = VideoFileClip(video_path)
        mp3_path = os.path.splitext(video_path)[0] + ".mp3"
        video_clip.audio.write_audiofile(mp3_path)

        return render_template("index.html", video_info=video_info, video_path=video_path, mp3_path=mp3_path)
    
    return render_template("index.html", video_info=None, video_path="", mp3_path="")

if __name__ == "__main__":
    app.run(debug=True)
