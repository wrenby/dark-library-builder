from datetime import datetime, timedelta
from dateutil.parser import parser
from time import strftime

# only necessary to run on the may 12/may 13 logfile
# fixes the offset from astroberry not using the rtc
# TODO: check if the date is also all right -- i think it is?

filename = "2022-05-12 11:43:56.txt"
offset = timedelta(hours=10, minutes=14, seconds=24)
with open(filename, 'r') as f:
    p = parser()
    pre, ext = filename.split(".")
    with open(f"{pre}-fixed.{ext}", 'w') as out:
        for line in f.readlines():
            time, temp = line.strip().split(" - ")
            time: datetime = p.parse(time)
            time += offset

            timestr = time.strftime("%Y-%m-%d %H:%M:%S")
            out.write(f"{timestr} - {temp}\n")
