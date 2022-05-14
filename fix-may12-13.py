from datetime import datetime, timedelta
from dateutil.parser import parser
from time import strftime

# only necessary to run on the may 12/may 13 logfile
# fixes the offset from astroberry not using the rtc
# TODO: check if the date is also all right -- i think it is?

filename = ""
offset = timedelta(hours=10, minutes=14, seconds=24)
with open(filename, 'r') as f:
    pre, ext = filename.split(".")
    with open(f"{filename}-fixed.{ext}", 'w') as out:
        for line in f.readlines():
            time, temp = line.strip().split(" - ")
            time: datetime = parser.parse(time)
            time += offset

            timestr = strftime("%Y-%m-%d %H:%M%S")
            out.write(f"{timestr} - {temp}\n")

