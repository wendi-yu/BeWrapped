import requests
import os

from moviepy.editor import *

class MemorySplicer:
    def __init__(self):
        self.photos = []

    def download_photos(self, url_list):
        for idx, url in enumerate(url_list):
            data = requests.get(url).content
            with open(f"secondary/{idx}.jpg", "wb") as f:
                f.write(data)

    def create_video(self):
        images = os.listdir("./secondary")
        clips = [ImageClip("./secondary/" + m).set_duration(0.1) for m in images]
        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile("test.mp4", fps=24)
        os.system("open test.mp4")