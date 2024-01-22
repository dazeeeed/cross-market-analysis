import json 
from datetime import datetime, timedelta

filename = "messages.txt"

with open(filename, "rb") as file:
    lines = [json.loads(line.decode('utf-8')) for line in file.readlines()]

times = [line.get("time") for line in lines][1:]
times = [datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ") for time in times]

diffs = [0]
for i, time in enumerate(times[:-1]):
    diff = - round((time - times[i+1]) / timedelta(milliseconds=1), 1)
    diffs.append(diff)

# Diffs in milliseconds, should be 50
print(diffs)