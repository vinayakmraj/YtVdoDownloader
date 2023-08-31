import os
from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import VideoFileClip

app = Flask(__name__)

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
        
        # Convert video to MP3
        video_clip = VideoFileClip(video_path)
        mp3_path = os.path.splitext(video_path)[0] + ".mp3"
        video_clip.audio.write_audiofile(mp3_path)
        
        status = "Video downloaded and converted to MP3 successfully!"
        return render_template("index.html", status=status)
    return render_template("index.html", status="")

if __name__ == "__main__":
    app.run(debug=True)
