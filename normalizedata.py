'''
data.csv time normalizer:
copy lines from data.csv, add time stamps + no data if there are gaps > 5 minutes 
'''

import sys
import time
import re
from datetime import datetime, timedelta


def get_date_time_str(line):
    date_time_str = ""
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),+"
    match = re.search(pattern, line)

    if match:
        date_time = match.group(1)
        date_time_str = date_time
    else:
        print("No match found")

    return date_time_str


def convert_date_time_to_string(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

records_interval = 300        # seconds
records_interval_error = 30 # seconds
delta = timedelta(seconds=records_interval + records_interval_error)

datafile = open("data.csv", "r")
datafilenorm = open("data_norm.csv", "w")

previous_line = datafile.readline().rstrip("/n")
previous_date_time_str = get_date_time_str(previous_line)
datafilenorm.write(previous_line)

skip_first_line = True

for line in datafile:
    if skip_first_line:
        skip_first_line = False
        datafilenorm.write(line)
        continue

    # Get date/time string from the line
    current_date_time_str = get_date_time_str(line.rstrip("/n"))

    if current_date_time_str == "":
        continue

    curr = datetime.strptime(current_date_time_str, "%Y-%m-%d %H:%M:%S")
    prev = datetime.strptime(previous_date_time_str, "%Y-%m-%d %H:%M:%S")
    if curr - prev > delta:
        # Add missing lines as dummy stubs
        nrofmissing = int(round((curr - prev) / delta, 0))
        for i in range(1, nrofmissing + 1):
            newdatetime = convert_date_time_to_string(prev + delta * i)
            print("adding missing line: ", newdatetime, i)
            # Keep only time stamp, no data
            datafilenorm.write("{},\n".format(newdatetime))
        datafilenorm.flush()
    
    # Keep current line, don't add anything
    datafilenorm.write(line)
    datafilenorm.flush()
    previous_date_time_str = current_date_time_str

datafile.close()
datafilenorm.close()
