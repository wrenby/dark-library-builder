from datetime import datetime
from dateutil.parser import parser
from time import strftime

# only necessary to run on the may 11/may 12 logfile
# fixes the datetime formatting to be in line with the newer file

filename = "2022-05-11 23:02:56.txt"
with open(filename, 'r') as f:
    pre, ext = filename.split(".")
    p = parser()
    with open(f"{pre}-fixed.{ext}", 'w') as out:
        for line in f.readlines():
            time, temp = line.strip().split(": ")
            time: datetime = p.parse(time)
            if time.hour > 12:
                time = time.replace(year=2022, month=5, day=11)
            else:
                time = time.replace(year=2022, month=5, day=12)

            timestr = time.strftime("%Y-%m-%d %H:%M:%S")
            out.write(f"{timestr} - {temp}\n")
