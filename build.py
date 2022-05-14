from datetime import datetime, timedelta
from dateutil import parser
from PIL import Image
# from PIL.ExifTags import TAGS
import os

# TODO: timezone offset?

TEMP_FOLDER = "./temps"
DARK_FOLDER = "./darks"
OUTPUT_FOLDER = "./dark-library"

ISO_TAG = 0x8827
EXP_TAG = 0x829A
TIME_TAG = 0x9003

temps = {}

for filename in os.walk(TEMP_FOLDER):
    if filename.endswith(".txt"):
        with open(filename, 'r') as f:
            for line in f.readlines():
                time, temp = line.strip().split(" - ")
                time = parser.parse(time)
                temps[time] = temp # just store as a string

for filename in os.listdir(DARK_FOLDER):
    src = f"{DARK_FOLDER}/{filename}"
    img = Image.open(src)
    exif = img.getexif()

    iso = exif[ISO_TAG]
    exp = round(exif[EXP_TAG]) # round to nearest second
    time = exif[TIME_TAG]
    nearest_key = min(temps.keys(), key=lambda x:abs(x-time)) # min probably doesn't do a binary search here, but idc about the performance loss
    temp = temps[nearest_key]

    img.close()
    # TODO: is this how i had these folders nested?
    folder = f"{OUTPUT_FOLDER}/{iso}ISO/{exp}s/{temp}C"
    dst = f"{folder}/{filename}"
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.replace(src, dst)
