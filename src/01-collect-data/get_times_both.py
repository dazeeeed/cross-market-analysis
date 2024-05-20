import json 
from datetime import datetime, timedelta
import utilities
import os
import matplotlib.pyplot as plt
import numpy as np

### PARAMETERS
draw_chart = True
draw_moving_avg = True
draw_median = True
###

data_path = utilities.get_data_path(tree_level=2)
filename = os.path.join(data_path, "messages-eth.txt")

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

if draw_chart:
	fig, ax = plt.subplots()
	diffs = np.array(diffs)

	if draw_moving_avg:
		diff_mov_avg = utilities.running_mean(diffs, 10)
		ax.plot(diff_mov_avg)
	else:
		ax.plot(diffs)
	
	if draw_median:
		median = np.median(diffs)
		ax.plot([0, diffs.shape[0]], [median for _ in range(2)], label="Mediana")

	plt.xlabel('Numer wiadomości')
	plt.ylabel('Opóźnienie [ms]')
	plt.legend()
	plt.show()
