#!/usr/bin/python

## Running the "sensors" terminal command from within Python script
import subprocess
import re
import datetime
import sys

cmd = subprocess.Popen(["sensors"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = cmd.communicate()

out = err = ""
if stderr is None:
    out = stdout.decode("utf-8")
else:
    err = stderr.decode("utf-8")

if out:
    re_result = re.findall(r"(.*\+[4-9]\d\.\d).C", out)
    now = str(datetime.datetime.now())[:-10]  # Truncate the seconds and fractional seconds
    if re_result:
        # N.B. If this code is run by cron as user earl, the sensors.out file will be in /home/earl
        with open("sensors.out", "a") as fp:
            fp.write("\n========= " + now + "\n")
            for res in re_result:
                fp.write(res + "\n")

elif err:
    with open("sensors.out", "a") as fp:
        fp.write("\n========= " + now + "\n")
        fp.write("The following error occurred while invoking 'sensors'\n")
        fp.write(err)
