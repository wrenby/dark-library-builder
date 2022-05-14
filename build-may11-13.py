from datetime import datetime, timedelta
from dateutil import parser
from PIL import Image
# from PIL.ExifTags import TAGS
import os

# TODO: timezone offset?
# ! only run on the may 11-13 dark frames,
# ! since it corrects for an error in the camera clock that was fixed on the morning of the 13th

TEMP_FOLDER = "./temps"
DARK_FOLDER = "./darks"
OUTPUT_FOLDER = "./dark-library"

CAMERA_CLOCK_WRONG_UNTIL = datetime(year=2022, month=5, day=13, hour=12)
CAMERA_DST_OFFSET = timedelta(hours=1)

ISO_TAG = 0x8827
EXP_TAG = 0x829A
TIME_TAG = 0x9003

temps = {}

p = parser()
for filename in os.walk(TEMP_FOLDER):
    if filename.endswith(".txt"):
        with open(filename, 'r') as f:
            for line in f.readlines():
                time, temp = line.strip().split(" - ")
                time = p.parse(time)
                temps[time] = temp # just store as a string

for filename in os.listdir(DARK_FOLDER):
    src = f"{DARK_FOLDER}/{filename}"
    img = Image.open(src)
    exif = img.getexif()
    print(exif)

    # TODO: what format is any of this shit
    iso = exif[ISO_TAG]
    exp = round(exif[EXP_TAG]) # round to nearest second
    time = exif[TIME_TAG]

    if time < CAMERA_CLOCK_WRONG_UNTIL:
        time += CAMERA_DST_OFFSET

    nearest_key = min(temps.keys(), key=lambda x:abs(x-time)) # min probably doesn't do a binary search here, but idc about the performance loss
    dist: timedelta = abs(time - nearest_key)
    if dist > timedelta(minutes=1):
        print(f"No temperature reading within a minute found for {filename} -- nearest was {dist.total_seconds():.0f} seconds away at {nearest_key}")

    temp = temps[nearest_key]

    img.close()
    # TODO: is this how i had these folders nested?
    folder = f"{OUTPUT_FOLDER}/{iso}ISO/{exp}s/{temp}C"
    dst = f"{folder}/{filename}"
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.replace(src, dst)
