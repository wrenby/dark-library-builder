from datetime import datetime
from dateutil.parser import parser
from time import strftime

# only necessary to run on the may 11/may 12 logfile
# fixes the datetime formatting to be in line with the newer file

filename = ""
with open(filename, 'r') as f:
    pre, ext = filename.split(".")
    with open(f"{filename}-fixed.{ext}", 'w') as out:
        for line in f.readlines():
            time, temp = line.strip().split(": ")
            time: datetime = parser.parse(time)
            if time.hour > 12:
                time.replace(year=2022, month=5, day=11)
            else:
                time.replace(year=2022, month=5, day=12)

            timestr = strftime("%Y-%m-%d %H:%M%S")
            out.write(f"{timestr} - {temp}\n")

