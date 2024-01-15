import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw

from moviepy.editor import *

MEM_URL = "./memories"
WRAPPED_FILE = "wrapped.mp4"

# video speed curve (inverted - clip durations)
def main_curve(l):
    return [max(1.61*(10**-9)*(x**4) - 1.61*(10**-6)*(x**3) + 0.00055*(x**2) - 0.065*x + 0.8, 0.09) for x in range(l)]

def initial_curve(l):
    return [0.05] * l

class MemorySplicer:
    def __init__(self):
        if not os.path.exists(MEM_URL):
            os.makedirs(MEM_URL)

    def download_photos(self, url_list):
        for idx, urls in enumerate(url_list):
            # get url contents
            primary_raw = requests.get(urls[0]).content
            secondary_raw = requests.get(urls[1]).content

            # create pillow images
            primary = Image.open(BytesIO(primary_raw))
            secondary = Image.open(BytesIO(secondary_raw))

            # resize and overlay secondary
            thumbnail_size = primary.height / 3
            secondary.thumbnail((thumbnail_size, thumbnail_size))

            # round corner mask
            mask = Image.new("L", secondary.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, secondary.width, secondary.height), fill=255, radius=30)

            primary.paste(secondary, (primary.width//20, primary.width//20), mask)

            # save
            primary.save(f"{MEM_URL}/{idx}.jpg")

    def create_video(self):
        images = os.listdir(MEM_URL)
        duration_curve = main_curve(len(images))
        clips = []
        # first timelapse chunk
        curve1 = initial_curve(15)
        for m, duration in zip(images[:15], curve1):
            clips.append(ImageClip(MEM_URL + "/" + m).set_duration(duration))
        # black screen
        black_duration = 2
        clips.append(ColorClip(clips[0].size, duration=black_duration, color=[0, 0, 0]))
        # main timelapse video - secondaries
        for m, duration in zip(images, duration_curve):
            clips.append(ImageClip(MEM_URL + "/" + m).set_duration(duration))
        concat_clip = concatenate_videoclips(clips, method="compose")

        # text overlay for first 3 seconds
        txt_clip = TextClip("2023\nRECAP",fontsize=300, color='white',font='DIN-Condensed-Bold').set_position('center').set_duration(sum(curve1) + black_duration)
        video = CompositeVideoClip([concat_clip, txt_clip])


        # write and open
        video.write_videofile(WRAPPED_FILE, fps=24)
        os.system(f"open {WRAPPED_FILE}")