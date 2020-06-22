#!/usr/bin/python3

# Change the permissions of this file so it's executable by cron, e.g.
# chmod a+x sensors.py

"""Execute the "sensors" terminal command from this Python script
and record the output in a file"""
import subprocess
import datetime
import re
import sys

OUT_FILENAME = "sensors.out"
now = str(datetime.datetime.now())[:-10]  # Truncate the seconds and fractional seconds

try:
    cmd = subprocess.Popen(["sensors"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = cmd.communicate()
except Exception as exc:
    msg = "Exception occurred while executing 'sensors' command"
    with open(OUT_FILENAME, "a") as fp:
        fp.write("\n========= " + now + "\n")
        fp.write(msg + "\n")
        fp.write(str(exc.args) + "\n")
    sys.exit(msg)

out = err = ""
if stderr is None:
    out = stdout.decode("utf-8")
else:
    err = stderr.decode("utf-8")

if out:
    re_result = re.findall(r"(.*\[^=] +[8-9]\d\.\d).C", out)
    if re_result:
        # N.B. If this code is run by cron as user earl, the sensors.out file will be in /home/earl
        with open(OUT_FILENAME, "a") as fp:
            fp.write("\n========= " + now + "\n")
            for res in re_result:
                fp.write(res + "\n")
else:
    with open(OUT_FILENAME, "a") as fp:
        fp.write("\n========= " + now + "\n")
        fp.write("The following error occurred while invoking 'sensors'\n")
        fp.write(err + "\n")
