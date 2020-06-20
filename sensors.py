#!/usr/bin/python

## Running the "sensors" terminal command from within Python script
import subprocess
import re
import datetime

cmd = subprocess.Popen(["sensors"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = cmd.communicate()

if stderr is None:
    out = stdout.decode("utf-8")
else:
    err = stderr.decode("utf-8")

re_result = re.findall(r"(.*\+[8-9]\d\.\d).C", out)

now = str(datetime.datetime.now())[:-10]  # Truncate the seconds and fractional seconds

print(now)
for res in re_result:
    print(res)

if re_result:
    # N.B. If this code is run by cron as user earl, the sensors.out file will be in /home/earl
    with open("sensors.out", "a") as fp:
        fp.write("\n========= " + now + "\n")
        for res in re_result:
            fp.write(res + "\n")
