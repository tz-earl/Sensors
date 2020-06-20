# Sensors
Python script to run the Linux `sensors` terminal command

Intended to be invoked repeatedly via the cron utility.

This little script was motivated by the desire to record and monitor
when CPU temperatures exceed a certain threshold, which is currently
hard-coded.

The output is appended to a text file.
